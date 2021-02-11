#!/usr/bin/perl
#
# cpufreq-utils, SmoothWall Express 3.1 mod for enabling and controling CPU scaling on supported processors
# (c) 2014 Peter Schofield
#
# Congratulations to Fest3er, s-t-p, wkitty42, panda, BoHiCa and all the others on the SWE forums who were involved in the long-awaited successful release of SWE 3.1!
#
# SmoothWall CGIs
#
# This code is distributed under the terms of the GPL
#
# (c) The SmoothWall Team
# cpufreq.cgi

my $release = "Version 1";

use lib "/usr/lib/smoothwall";
use header qw( :standard );

my %cgiparams;

my $title = "CPU Frequency Scaling";

my $scriptdir = "/usr/bin/smoothwall";
# the prefs_file should be -rw-rw-rw- (666)
my $prefs_file = "${swroot}/cpufreq-utils/preferences/stored";

&set_prefs_default();

$cgiparams{'ACTION'} = " " ;
&getcgihash(\%cgiparams);
&get_prefs_from_cgi();

########################
#      vars			   #
########################

my @governors = split(' ',`cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_available_governors`);
my @speeds = reverse(split(' ',`cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_available_frequencies`));
my @limits = (`cat /sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_min_freq`,`cat /sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_max_freq`);
my $currentgovernor = "".`cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor`;
my $currentspeed = `cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq`;
my @currentrange = (`cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_min_freq`,`cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_max_freq`);
my $currentdriver = `cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_driver`;
my @loadavg = split(' ',`cat /proc/loadavg`);
chomp(@limits);

&showhttpheaders();

&openpage($tr{'CPUFreq-utils'}."$title", 1, ' <META HTTP-EQUIV="Cache-Control" content="no-cache"> <META HTTP-EQUIV="Pragma" CONTENT="no-cache"> ', 'about your smoothie');

&openbigbox('100%', 'LEFT');
&alertbox($errormessage);

   &openbox($tr{'CPUFreqc'}." $release");

   print "<h2>Current Status</h2>";

print "Load Avarage:&emsp;1 min&emsp;5 min&emsp;15 min<br/>";
print "&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;$loadavg[0]&emsp;$loadavg[1]&emsp;&emsp;$loadavg[2] <br/>";
print "Hardware Minimum Speed: ",friendly_numbers($limits[0]),"<br/>";
print "Hardware Maximum Speed: ",friendly_numbers($limits[1]),"<br/>";
print "CPUFreq Driver: $currentdriver <br/>";
print "Current Governor: $currentgovernor<br/>";
print "Current Speed: ",friendly_numbers($currentspeed),"<br/>";
print "Available Minimum Speed ",friendly_numbers($currentrange[0]),"<br/>";
print "Available Maximum Speed ",friendly_numbers($currentrange[1]),"<br/>";
#print "Detected Driver: ",detect_driver(),"<br/>";

  &closebox();

 &openbox('');

print "<h2>Dynamic Processor Speed</h2>";
print "<form method=\"POST\" action=\"\" onsubmit=\"return validate(this.policy,this.newminfreq,this.newmaxfreq)\">";

if ($currentgovernor ne 'userspace')
{
	print "<input type=\"radio\" name=\"policy\" value=\"dynamic\" checked> Use dynamic processor frequency scaling<br/>";
}
else
{
	print "<input type=\"radio\" name=\"policy\" value=\"dynamic\"> Use dynamic processor frequency scaling<br/>";
}
print "&emsp;&emsp;Governor: <select name=\"newgovernor\">";
foreach my $element (@governors)
{
	chomp($element);
	$element = "".$element;
	$currentgovernor =~ s/\r|\n|\s//g;
	$element =~ s/\r|\n|\s//g;
	if($element eq 'userspace')
	{
		next;
	}
	#hack time, if $element eq $currentgovernor never returns true, even when strings are byte for byte identical. Unpacking both and then comparing arrays works.
	my @array1 = unpack("C*", $currentgovernor);
	my @array2 = unpack("C*", $element);
	if(@array1 ~~ @array2)
	{
		print "<option value=\"$element\" selected>$element</option>";
	}
	else
	{
		print "<option value=\"$element\">$element</option>";
	}
}
print "</select><br/>";
print "&emsp;&emsp;Minimum frequency: <select name=\"newminfreq\">";
foreach my $element (@speeds)
{
	$element = $element+0;
	if($element >= $currentrange[1])
	{
		next;
	}
	if($element == $currentrange[0])
	{
		print "<option value=\"$element\" selected>",friendly_numbers($element),"</option>";
	}
	else
	{
		print "<option value=\"$element\">",friendly_numbers($element),"</option>";
	}
}
print "</select><br/>";
print "&emsp;&emsp;Maximum frequency: <select name=\"newmaxfreq\">";
foreach my $element (@speeds)
{
	$element = $element+0;
	if($element <= $currentrange[0])
	{
		next;
	}
	if($element == $currentrange[1])
	{
		print "<option value=\"$element\" selected>",friendly_numbers($element),"</option>";
	}
	else
	{
		print "<option value=\"$element\">",friendly_numbers($element),"</option>";
	}
}
print "</select><br/>";

  &closebox();

 &openbox('');

print "<h2>Fixed Processor Speed</h2>";
if ($currentgovernor eq 'userspace')
{
	print "<input type=\"radio\" name=\"policy\" value=\"fixed\" checked> Use a fixed processor speed<br/>";
}
else
{
	print "<input type=\"radio\" name=\"policy\" value=\"fixed\"> Use a fixed processor speed<br/>";
}
print "&emsp;&emsp;Fixed processor frequency: <select name=\"newfixedfreq\">";
foreach my $element (@speeds)
{
	$element = $element+0;
	if($element == $currentspeed)
	{
		print "<option value=\"$element\" selected>",friendly_numbers($element),"</option>";
	}
	else
	{
		print "<option value=\"$element\">",friendly_numbers($element),"</option>";
	}
}
print "</select><br/>";
  &closebox();

 &openbox('');
 
 print "<input type=\"submit\" name=\"ACTION\" value=\"Save\">";
 print "</form><script language=javascript>
function validate(policy,min,max){
	if (policy.value == 'fixed')
	{
		return true;
	}
	if (int(max.value) < int(min.value)) 
	{
		alert(\"My apologies, Captain, it is illogical to set the minimum frequency higher than the maximum frequency, therefore I am unable to comply with your request \");
		return false;
	}
	if (min.value == max.value) 
	{
		alert(\"This configuration is pointless, if you wish to set a static frequency please use the bottom half of the page\");
		return false;
	}
	return true;
	
}</script>";
 	
	&closebox();

&alertbox('add','add');
&closebigbox();
&closepage();


###############################################
#             logic functions                 #
###############################################

sub friendly_numbers
{
	my $friendly = (0+$_[0])/1000;
	if (length($friendly) >= 4)
	{
		$friendly = $friendly/1000;
		$friendly .= 'Ghz';
	}
	else
	{
		$friendly .= 'Mhz';
	}
	return $friendly;
}

sub write_prefs_file() {
	if (open(FILE, ">${prefs_file}"))
	{
		flock FILE, 2;
		if ($_[0] eq 'dynamic')
		{
			print FILE "$cgiparams{'newgovernor'}\n$cgiparams{'newminfreq'}\n$cgiparams{'newmaxfreq'}";
			#print "$cgiparams{'newgovernor'},$cgiparams{'newminfreq'},$cgiparams{'newmaxfreq'}";
		}
		elsif ($_[0] eq 'fixed')
		{
			print FILE "$cgiparams{'newgovernor'}\n$cgiparams{'newfixedfreq'}";
			#print "$cgiparams{'newgovernor'},$cgiparams{'newfixedfreq'}";
		}
		close FILE;
	} else { 
		$errormessage = "Unable to open $prefs_file for writing";
	}
}

sub get_prefs_from_cgi() {
     if ($cgiparams{'ACTION'} eq "Save" )
	 {
	    my $policy = $cgiparams{'policy'};
		if ($cgiparams{'policy'} eq "dynamic" ) 
		{
			my $cmd = "cpufreq-set -g $cgiparams{'newgovernor'} -d $cgiparams{'newminfreq'} -u $cgiparams{'newmaxfreq'}";
			#print $cmd
			system($cmd);
	    } 
		elsif ($cgiparams{'policy'} eq "fixed" ) 
		{
			system("cpufreq-set -g userspace");
			my $cmd = "cpufreq-set -f $cgiparams{'newfixedfreq'}";
			#print $cmd
			system($cmd);
		}
		&write_prefs_file($policy) ;
	}
}

sub set_prefs_default() 
{
	if ( -z $prefs_file == 1)
	{
		open(FILE, ">${prefs_file}");
		flock FILE, 2;
		print FILE "ondemand\n$limits[0]\n$limits[1]";
		close FILE;
	}
}

sub detect_driver()
{
my $driver = '';
my $linux = `uname -r`;
my $vendor = '';
my $model = '';
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
my $vendor = $cpuinfo{'vendor_id'};
$model = $cpuinfo{'model_name'};
my @cpuflags = split(' ',$cpuinfo{'flags'});

if ($vendor eq 'GenuineIntel')
{
	$driver = 'speedstep-lib';
	foreach (@cpuflags)
	{
		if ($_ eq 'est')
		{
			$driver = 'acpi-cpufreq';
			last;
		}
	}
	if (grep($_ eq 'est', @cpuflags))
	{
		my $driver = 'acpi-cpufreq';
	}
	if ($model =~ /Core\(TM\) i/) #hope this works, cant test
	{
		my $driver = 'intel_pstate';
	}
}
elsif ($vendor eq 'AuthenticAMD') #also hope this works
{
	my $driver = 'powernow-k8';
	if ($linux >= 3.7.0)
	{
		my $driver = 'acpi-cpufreq';
	}
}
else
{
	#uhh dunno what this processor is... LAST CALL, USS make sh*t up is now boarding!
	my $driver = 'acpi-cpufreq'; #when in doubt, Intel. I think.
}
return $driver;
}
