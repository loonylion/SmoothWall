#!/usr/bin/perl
#
# ssd.cgi, SmoothWall Express 3.1+ integration for enabling and controlling the 'trim' feature on supported SSDs. Basically a UI for the integration of panda's ssdtrim mod
# (c) 2021 Peter Schofield
#
# SmoothWall CGIs
#
# This code is distributed under the terms of the GPL
#
# (c) The SmoothWall Team
# ssd.cgi

my $release = "Version 1";

use lib "/usr/lib/smoothwall";
use header qw( :standard );

my %cgiparams;

my $title = "SSD Trim Configuration";

my $scriptdir = "/usr/bin/smoothwall";
# the prefs_file should be -rw-rw-rw- (666)
my $prefs_file = "${swroot}/ssdtrim/preferences/stored";

&set_prefs_default();

$cgiparams{'ACTION'} = " " ;
&getcgihash(\%cgiparams);
&get_prefs_from_cgi();

########################
#      vars			   #
########################

my @options = ("Disabled","Enabled","Forced");
my $isEnabled = -e "/var/smoothwall/ssdtrim/enabled";
my $isForced = -e "/var/smooothwall/ssdtrim/forced";
my $isSupported = -e "/var/smoothwall/ssdtrim/supported";
my $status = 'Disabled';
if ($isEnabled && $isSupported)
{
	status = 'Enabled'; 
}
elsif ($isEnabled && !$isSupported)
{
	status = 'Forced';
}
else
{
	my status = 'Disabled';
}
my $currentsetting = $status;
my $supportDisplay;
if ($isSupported) 
{
	$supportDisplay = '<font colour="green"><strong>Supported</strong></font>';
}
else
{
	$supportDisplay = '<font colour="red"><strong>Not Supported</strong></font>';
}

&showhttpheaders();

&openpage($tr{'ssdtrim'}."$title", 1, ' <META HTTP-EQUIV="Cache-Control" content="no-cache"> <META HTTP-EQUIV="Pragma" CONTENT="no-cache"> ', 'about your smoothie');

&openbigbox('100%', 'LEFT');
&alertbox($errormessage);

   &openbox($tr{'SSDTrim'});

   print "<h2>Current Status</h2>";

print "Your drive reports that Trim is: ",$supportDisplay,"<br/>";
if (!$isSupported)
{
print "Not all SSDs that support Trim report it correctly, or the detection may have been wrong. Some rotating HDDs also report Trim support (DM-SMR drives) when they shouldn't.<br/>if you KNOW you have an SSD that you KNOW supports Trim, set the option to 'Forced' <br/>Do NOT do this on a rotating HDD <br/>Also not advisable on CF/SD/mSD/USB sticks etc as these generally don't do trim<br/>";
}
print "FS Trim is: ",$status,"<br/>";

  &closebox();

 &openbox('');

print "<h2>SSD Trim status</h2>";
print "<form method=\"POST\" action=\"\" onsubmit=\"return validate(this.ssdtrim)\">";

print "&emsp;&emsp;SSD Trim feature: <select name=\"ssdtrim\">";
	foreach my $element (@options)
{
	chomp($element);
	$element = "".$element;
	$currentsetting =~ s/\r|\n|\s//g;
	$element =~ s/\r|\n|\s//g;
	#hack time, if $element eq $currentsetting never returns true, even when strings are byte for byte identical. Unpacking both and then comparing arrays works.
	my @array1 = unpack("C*", $currentsetting);
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

  &closebox();

 &openbox('');
 
 print "<input type=\"submit\" name=\"ACTION\" value=\"Save\">";
 print "</form><script language=javascript>
function validate(ssdtrim){
	switch (String(ssdtrim))
	{
		case \"enabled\":
		case \"disabled\":
		case \"forced\":
			return true;

		default:
			alert(\"Invalid value, please don't tamper with the select box\"
	}
	}</script>";
 	
	&closebox();

&alertbox('add','add');
&closebigbox();
&closepage();


###############################################
#             logic functions                 #
###############################################


sub write_prefs_file() {
	if (open(FILE, ">${prefs_file}"))
	{
		flock FILE, 2;
		print FILE "$cgiparams{'ssdtrim'}";
		close FILE;
	} else { 
		$errormessage = "Unable to open $prefs_file for writing";
	}
}

sub get_prefs_from_cgi() {
     if ($cgiparams{'ACTION'} eq "Save" )
	 {
	    my $policy = $cgiparams{'ssdtrim'};
		if ($cgiparams{'ssdtrim'} eq "enabled" ) 
		{
			my $cmd = "touch ${swroot}/ssdtrim/enabled";
			#print $cmd
	    } 
		elsif ($cgiparams{'ssdtrim'} eq "forced" ) 
		{
			my $cmd = my $cmd = "touch ${swroot}/ssdtrim/forced";
			#print $cmd			
		}
		else
		{
			my $cmd = my $cmd = "rm ${swroot}/ssdtrim/{enabled|forced}";
		}
		system($cmd);
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
