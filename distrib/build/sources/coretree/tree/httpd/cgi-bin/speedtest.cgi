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

my $title = "WAN Speedtest";

my $scriptdir = "/usr/bin/smoothwall";
# the prefs_file should be -rw-rw-rw- (666)
#my $prefs_file = "${swroot}/cpufreq-utils/preferences/stored";

#&set_prefs_default();

$cgiparams{'ACTION'} = " " ;
&getcgihash(\%cgiparams);
&get_prefs_from_cgi();

if (!exists("/tmp/speedtest"))
{
	`speedtest -f csv >/tmp/speedtest`;
	&showhttpheaders();
	&openpage($tr{'Speedtest'}."$title", 1, '<META REFRESH="20" <META HTTP-EQUIV="Cache-Control" content="no-cache"> <META HTTP-EQUIV="Pragma" CONTENT="no-cache"> ', 'about your smoothie');

&openbigbox('100%', 'LEFT');
&alertbox($errormessage);

   &openbox($tr{'Speedtest'});

   print "<h2>Speedtest in progress, reloading page in 20 seconds</h2>";
   &closebox();

&alertbox('add','add');
&closebigbox();
&closepage();
}

########################
#      vars			   #
########################

my @results = split(',',`cat /tmp/speedtest`);

&showhttpheaders();

&openpage($tr{'Speedtest'}."$title", 1, ' <META HTTP-EQUIV="Cache-Control" content="no-cache"> <META HTTP-EQUIV="Pragma" CONTENT="no-cache"> ', 'about your smoothie');

&openbigbox('100%', 'LEFT');
&alertbox($errormessage);

   &openbox($tr{'Speedtestc'});

   print "<h2>Speedtest Results:</h2>";
print "<p>Speedtest server: ",@results[1],"</p><br/>";
print "<table><tr><th rowspan=\"2\">Latency (ms)</th><th rowspan=\"2\">Jitter (ms)</th><th rowspan=\"2\">Packet Loss</th><th colspan=\"2\">Download</th><th colspan=\"2\">Upload</th></tr>
<tr><th>Speed</th><th>Bytes</th><th>Speed</th><th>Bytes</th></tr>";
print "<tr><td>",@results[2],"</td><td>",@results[3],"</td><td>",@results[4]," </td><td>",friendly_numbers(@results[5]),"bps</td><td>",friendly_numbers(@results[6]),"bytes</td><td>",friendly_numbers(@results[7]),"bps</td><td>",friendly_numbers(@results[8]),"bytes</td></tr></table></div>";
  &closebox();

# &openbox('');
 
 #print "<input type=\"submit\" name=\"ACTION\" value=\"Re-run\">";
 #print "</form>";
 	
#	&closebox();

&alertbox('add','add');
&closebigbox();
&closepage();


###############################################
#             logic functions                 #
###############################################

sub friendly_numbers
{
	my $friendly = (0+$_[0])/1000;
	if (length($friendly) >= 8)
	{
		$friendly = $friendly/1000;
		$friendly .= 'T';
	}
	elsif (length($friendly) >= 6)
	{
		$friendly = $friendly/1000;
		$friendly .= 'G';
	}
	elsif (length($friendly) >= 4)
	{
		$friendly = $friendly/1000;
		$friendly .= 'M';
	}
	elsif (length($friendly) >= 2)
	{
		$friendly = $friendly/1000;
		$friendly .= 'K';
	}
	else
	{
		$friendly .= '';
	}
	return $friendly;
}

sub get_prefs_from_cgi() {
     if ($cgiparams{'ACTION'} eq "Re-run" )
	 {
	    `rm /tmp/speedtest`;
	    #refresh page somehow.
	}
}
