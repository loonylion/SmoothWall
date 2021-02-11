!#/usr/bin/perl
#
# This code is distributed under the terms of the GPL
#
# (c) peter schofield 2021
# (c) 
#
use Getopt::Long


my $mode = @ARGV[0];
my runmode = 'auto_all';
if ($mode eq 'fulliautomatix';
	{
		#tries to autodetect everything and guess the best config
		$runmode = 'auto_all';
	}
else if ($mode eq 'advanced')
	{
		#guided, asks questions and gives choices. Will try not to allow dangerous configs eg 'no rdrand' + 'no haveged' + 'no rngtools' + 'no hw trng' or rdrand only with a dodgy implementation
		$runmode = 'auto_adv';
	}
else if ($mode eq 'manual')
	{
		#does only as its told, expects all options in cmdline. If you ask for a dangerous config, you'll get it. not implemented yet
		#$runmode = 'man';
		$runmode = 'auto_all';
	}
else {
		$runmode = 'auto_all';
	}
my $linux = `uname -r`;
my $vendor = '';
my $model = '';
my $rdrand = false; #true if cpu has rdrand
my $trustrdrnd = true; #true if rdrand is trustworthy
my $hwtrng = false; #true if physical hw true rng present
my $haveged = true; #true if enabling haveged
my $rngtools = false; #true if enabling rng-tools
my $nordrand = false; #true if rdrand isn't safe/usable, will set nordrand kernel option
my $refuserdrnd = false; #true if user doesn't trust/want rdrand, also sets nordrand kernel option
my $rngtoolscmd = '/usr/bin/rngd -b';
my $rngtoolspid = '--pid-file=';
my $havegedcmd = '/usr/bin/haveged';
my $cpuinfo = getCPUInfo();
sub getCPUInfo {
	#print "Checking /proc/cpuinfo for cpu specifics\n";
	open (CPUINFO, "</proc/cpuinfo") || die "Can't open file \/proc\/cpuinfo!! :
	$!\n";
	while (<CPUINFO>) 
	{
		chomp;
		$linetest = $_;
		if ($linetest=~ m/:/)
		{
			($key, $value) = split /\s*:\s*/;
			for ($key) 
			{
				$key =~ s/ /_/;
			}
        	$cpuinfo{$key} = $value;
    	}
	}
	close (CPUINFO);
	return $cpuinfo;
}
my $vendor = $cpuinfo{'vendor_id'};
$model = $cpuinfo{'model_name'};
my @cpuflags = split(' ',$cpuinfo{'flags'});
sub getBadRNGs {
	open (BADRNG, "</var/smoothwall/rdrand-test/badrngs.lst") || die "Can't open file \/var/smoothwall\/rdrand-test\/badrngs.lst!! :
	$!\n";
	my @badrngs = <BADRNG>;
	return @badrngs;
}
my $cpuid = $cpuinfo{'vendor_id'},":",$cpuinfo{'cpu family'},":",$cpuinfo{'model'},":",$cpuinfo{'stepping'};
sub isBadRNG {
	my (cpuid) = @_;
	@badrngs = getBadRNGs();
	foreach (@badrngs)
	{
		if (substr($_,0,1) eq '#';)
		{
			next;
		}
		if ($_ eq $cpuid)
		{
			return true;
			last;
		}
	}
	if (grep($_ eq $cpuid, @badrngs))
	{
		return true;
	}
	return false;
}
sub isRdRandSupported {
	my $cpuinfo = getCPUInfo();
	my @cpuflags = split(' ',$cpuinfo{'flags'});
	foreach (@cpuflags)
	{
		if ($_ eq 'rdrand')
		{
			return true;
			last;
		}
	}
	if (grep($_ eq 'rdrand', @cpuflags))
	{
		return true;
	}
}
sub genCPUID {
	my $cpuinfo = getCPUInfo();
	my $cpuid = $cpuinfo{'vendor_id'},":",$cpuinfo{'cpu family'},":",$cpuinfo{'model'},":",$cpuinfo{'stepping'};
	return $cpuid;
}

sub $canTrustRdRand {

	my ($vendor) = @_;
	my $cantrust = true;
	if ($vendor eq "AuthenticAMD")
	{
		#some amd chips had faulty rngs that return the same number every time, this was fixed by microcode. but test anyway
		my $amdtest = `/var/smoothwall/test-rdrand/amd-rdrand-bug`;
		if (($? >> 8) eq 0)
		{
			#good
		}
		else
		{
			#non-zero return code, either amd bug or rdrand didnt work but don't trust feature
			$cantrust = false
		}
	}
	
	#test rdrand output.
	my $output = `/var/smoothwall/test-rdrand/test-rdrand`;
	if (($? >> 8) == 0)
	{
		my @lines = split(\n,$output);
		my $firstsize = @lines;
		my %hash = map { $_, 1 } @lines;
		my @unique = %hash;
		my $secondsize = @unique;
		if ($firstsize != $secondsize)
		{
			#rdrand produced duplicate numbers, do not trust
			$cantrust = false;
		}
		# now check numbers are not sequential.
		my @numbers;
		my @parts;
		for ($element in @lines)
		{
			@parts = split(' ',$element)
			@numbers[] = @parts[2];
		}
		my @hamdistances
		for my $count (0 .. scalar @numbers -1)
		{
			#ideally should be doing this recursively on every element with every other element, not just consecutive ones, but might be too slow
			#hamdistances[] = ham_dist(@numbers[$count],@numbers[$count-1]);
			for my $count2 (0 .. scalar @numbers -1)
			{
				hamdistances[] = ham_dist(@numbers[$count],@numbers[$count2]);
			}
		}
		my $lowhamdist = 0;
		foreach @hamdistances
		{
				#check all hamming distances are above 3, otherwise not enough variation to be trustworthy. rdrand output is an 8 character hex string, 5 identical chars between two strings should not be happening. Absolutely not twice in any given sample.
			if ($_ < 3)
			{
				$lowhamdist++;
			}
		}
		if ($lowhamdist > 1)
		{
			$cantrust = false;
		}
	}
	else
	{
		#nonzero return, don't trust rdrand
		$cantrust = false;
	}
	return $cantrust;
}

if ($mode eq 'auto_all')
{
	if (isRdRandSupported())
	{
		$rdrand = true;
		if (isBadRNG())
		{
			$trustrdrnd = false;
		}
		else
		{
			$trustrdrnd = canTrustRdRand($vendor);
		}
	}
	else
	{
		#no rdrand available, or its not reporting as available
	}
	$hwtrng = haveHwTRNG();
	
	#now make decisions. basic logic: no/unsafe rdrand = haveged, unless hw trng, rdrand ok = rng-tools, hw trng = rng-tools.
	my $install = 1;
	if ($rdrand eq true && $trustrdrnd eq true)
	{
		$install = 2;
	}
	if ($hwtrng eq true)
	{
		if ($rdrand eq true && $trustrdrnd eq true)
		{
			$install = 2;
		}
		else
		{
			$install = 4;
		}
	}
	DoInstall($install);

if ($hwtrng eq true)
{
	$haveged = false;
	$rngtools = true;
}
sub instHaveged
{
	#enable haveged, write haveged cmd to startup file
	system ("echo \"",$havegedcmd, "\" > /etc/rc.d/02rc.sysinit");
}
sub instRngTools 
{
	my ($enablerdrand) = @_;
	$enablerdrand //= true;
	my $rngoption = '';
	if ($enablerdrand eq true)
	{
		$rngoption = ' -O rdrand:use-aes:1';
	}
	else if ($enablerdrand eq false)
	{
		$rngoption = ' -x rdrand';
	}
	my $rngtoolsfullcmd = $rngtoolscmd.$rngoption.$rngtoolspid;
	system ("echo \"",$rngtoolsfullcmd, "\" > /etc/rc.d/02rc.sysinit");
	#enable rng-tools, write command to startup file
}
if ($hwtrng eq true)
{
	#enable hw trng
}
sub hamdist {
	my(value1,$value2) = @_;
	my @1 - split(//,$value1);
	my @2 - split(//,$value2);
	
	my $hamdist = 0;
	
	for my $i (0 .. scalar @1 -1) {
		$hamdist += 1 if @1[$i] ne @2[$i];
	}
	return $hamdist
}
sub spanishinquisition {
	#asks questions for guided mode
	
	#questions:
	#use rdrand (y/n) (override if not detected or not desired)
	#use hw trng
	#use haveged or rng-tools
	
	print "Retrieving CPU Info from /proc/cpuinfo:"
	my $cpuinfo = getCPUInfo();
	print " Done\n";
	print "Checking for RDRAND/RDSEED support:"
	my $hasrdrnd = isRdRandSupported();
	my skiptonext = false;
	$rdrand = $hasrdrnd;
	if ($hasrdrnd eq false) {
		print "Not Supported\n";
		print "It appears that RDRAND is not present on this CPU. Do you agree with this assessment? If you don't know then you should say 'Yes', as it is probably correct and is the safer option. Only say 'No' if you know for certain your CPU has RDRAND (y/n)"
		while (<>)
		{
			chomp($_);
			if ($_ =~ /^y(?:es)?$/i)
			{
				print "\nconfirmed RDRAND unsupported, proceeding\n";
				$hasrdrnd = false;
				my $stage1 = false;
				last;
			}
			elsif ($_ =~ /^n(?:o)?$/i)
			{
				print "\nOVERRIDE: User indicated RDRAND support, proceeding\n";
				$hasrdrnd = true;
				my $stage1 = true;
			
			}
		}
	}
	if ($hasrdrand eq true)
	{
		print "It appears that RDRAND is present on this CPU. Checking implementation:\n";
		print "		Getting CPUID:";
		my $cpuid = genCPUID();
		print " Done.\n";
		print "		Checking CPUID against known bad implementations:";
		my $badrng = isBadRNG($cpuid);
		if ($badrng eq true)
		{
			
			print " Found\n";
			print "Unfortunately your CPU is known to have a faulty or unsafe implementation of RDRAND, it is highly recommended that you disable RDRAND support. Do you wish to disable RDRAND? (y/n)\n";
		while (<>)
		{
			chomp($_);
			if ($_ =~ /^y(?:es)?$/i)
			{
				print "\nconfirmed disable RDRAND, proceeding\n";
				$hasrdrnd = false;
				$trustrdrnd = false;
				my skiptonext = true;
				my $stage2 = false;
		
				last;
			}
			elsif ($_ =~ /^n(?:o)?$/i)
			{
				print "\nOVERRIDE: User indicated to use RDRAND, proceeding\n";
				$hasrdrnd = true;
				$trustrdrnd = true;
				my $stage2 = true;
				
			
			}
		}
		}
		if ($badrng eq false)
		{
			print "Not found, proceeding\n";
		}
		if (!$skiptonext)
		{
			print "RDRAND implementation not known to be bad or user overrode known bad implementation, testing implementation: (tech details: generate 20 random numbers using RDRAND, check theres no duplicates and not more than 1 pair has a hamming distance below 3)"
			my $test = canTrustRdRand($vendor);
			if ($test eq true)
			{
				print "Passed\n"
				print "Your RDRAND implementation appears to be ok to use. However, some people do not trust it and would prefer to disable it anyway, if this applies to you, say 'No' here. Do you wish to use RDRAND? (y/n):\n"
				while (<>)
				{
					chomp($_);
					if ($_ =~ /^y(?:es)?$/i)
					{
						print "\nconfirmed using RDRAND, proceeding\n";
						$hasrdrnd = true;
						$trustrdrnd = true;
						my $stage3 = true;
				
						last;
					}
					elsif ($_ =~ /^n(?:o)?$/i)
					{
						print "\nOVERRIDE: User indicated disable RDRAND, proceeding\n";
						$hasrdrnd = false;
						$trustrdrnd = false;
						my $stage3 = false;
					
					}
				}
			}
			else
			{
				print "FAILED\n"
				print "Your RDRAND implementation appears to be flawed. It is HIGHLY, HIGHLY recommended you disable RDRAND by saying 'No' here. Do you wish to USE RDRAND? (y/n):\n"
				while (<>)
				{
					chomp($_);
					if ($_ =~ /^y(?:es)?$/i)
					{
						print "\nconfirmed using RDRAND, proceeding\n";
						$hasrdrnd = true;
						$trustrdrnd = false;
						my $stage4 = true;
				
						last;
					}
					elsif ($_ =~ /^n(?:o)?$/i)
					{
						print "\nOVERRIDE: User indicated disable RDRAND, proceeding\n";
						$hasrdrnd = false;
						$trustrdrnd = false;
						my $stage4 = false;
					
					}
				}
			}
		}
	}
	my $userdrand = false;
	print "Summary:\n";
	print "--------\n";
	print "\n";
	print "CPU reports RDRAND present:",$rdrand,"\n";
	print "User confirmed RDRAND present:",$hasrdrnd,"\n";
	if ($hasrdrnd eq false)
	{
		print "RDRAND not present, not using RDRAND\n";
		print "end of summary\n";
	}
	else
	{
		print "CPU has known bad RDRAND: ",$badrng,"\n";
		if (skiptonext)
		{
			print "RDRAND known faulty or unsafe, not using RDRAND\n";
			print "end of summary\n";
		}
		else
		{
			print "RDRAND implementation passed tests: ",$test,"\n";
			if (!test && stage4 eq false)
			{
				print "RDRAND appears faulty or unsafe, not using RDRAND\n";
				print "end of summary\n";
			}
			else
			{
				print "Using RDRAND\n";
				print "end of summary\n";
				$userdrand = true;
			}
		}
	}
	#detect hwtrng
	print "Do you have a hardware true RNG device (HW TRNG)? If you don't know what one is then you don't have one. (y/n):\n";
	while (<>)
	{
		chomp($_);
		if ($_ =~ /^y(?:es)?$/i)
		{
			my $havehwtrng = true;
			last;
		}
		elsif ($_ =~ /^n(?:o)?$/i)
		{
			my havehwtrng = false;
		}
	}
	print "Summary:\n";
	print "--------\n";
	print "\n";
	if ($havehwtrng eq false)
	{
		print "Hardware TRNG not present, not using HW TRNG\n";
		print "end of summary\n";
	}
	else
	{
		print "HW TRNG detected or user confirmed presence, using HW TRNG\n";
		print "end of summary\n";
	}
	print "\n";
	print "Final summary:\n";
	print "--------------\n";
	print "\n";
	my $installtool = 'Haveged';
	my $reason;
	my $installindex =1; #1 = haveged, 2 = rng-tools, 3 = both, 4 = rng-tools without rdrand, 5 = 4+1
	if ($userdrand eq false)
	{
		$installtool = 'Haveged';
		$installindex = 1;
		$reason = 'do not have or do not want to use RDRAND, or it is not safe to use';
	}
	else
	{
		$installtool = 'RNG-Tools';
		$installindex = 2;
		$reason = 'have RDRAND, it seems safe to use and you are happy to use it';
	}
	if (havehwtrng eq true)
	{
		if ($userdrand eq false)
		{
			$installtool = 'RNG-Tools without RDRAND';
			$installindex = 4;
			$reason = 'have a HW TRNG but do not have or do not want to use RDRAND, or it is not safe to use';
		}
		else
		{
			$installtool = 'RNG-Tools';
			$installindex = 2;
			$reason = 'have a hardware TRNG, have RDRAND that seems safe to use, and are happy to use it';
		}
	}
	print "Based on your answers, it is recommended to install: ",$installtool,". I have decided this because you told me: you ",$reason",.\n"
	print "Are you happy to proceed with this recommendation (Advanced users may choose NO and pick their own software)(y/n)\n";
	while (<>)
	{
		chomp($_);
		if ($_ =~ /^y(?:es)?$/i)
		{
			doInstall($installindex);
			last;
		}
		elsif ($_ =~ /^n(?:o)?$/i)
		{
			print "Chose which package to install:\n";
			print "\n";
			print "Haveged\n";
			print "RNG-Tools (with RDRAND)\n";
			print "Haveged + RNG-Tools (with RDRAND)\n";
			print "RNG-Tools (without RDRAND)\n";
			print "Haveged + RNG-Tools (without RDRAND)\n";
			print "\n";
			while (<>)
			{
				chomp($_);
				if ($_ =~ /^h(?:aveged)?$/i)
				{
					doInstall(1);
					last;
				}
				elsif ($_ =~ /^r(?:ng-tools (with RDRAND)?$/i)
				{
					$doInstall(2);
					last;
				}
				elsif ($_ =~ /^b(?:oth)?$/i)
				{
					doInstall(3);
					last;
				}
				elsif ($_ =~ /^n(?:o RDRAND - RNG-tools)?$/i)
				{
					doInstall(4);
					last;
				}
				elsif ($_ =~ /^f(?:ull monty - RNG-tools with RDRAND, haveged)?$/i)
				{
					doInstall(5);
					last;
				}
			}
		}
	}
}
sub DoAsInstructed {
#no detection, no sanity checking, just take the given options and do it. unspecified options use defaults.
}
sub haveHwTRNG {
	return false;
}
sub doInstall {
	my ($installindex) = @_;
	
	if ($install eq 'haveged')
	{
		instHaveged();
	}
	else
	{
		if ($trustrdrnd eq false || $refusedrdrnd eq true)
		{
			instRngTools(false);
			system("sed -i '/^vmlinuz-/ s/$/ nordrand/' /boot/grub/grub.cfg");
		}
		else
		{
			instRngTools(true);
		}
	}
}
