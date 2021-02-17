#!/usr/bin/perl
# 
# SmoothWall CGIs
#
# This code is distributed under the terms of the GPL
#
# (c) The SmoothWall Team
# credits.cgi

use lib "/usr/lib/smoothwall";
use header qw( :standard );
use strict;
use warnings;

my $name = '';
my $title = 'Smoothwall Express 3.2 Credits';

&showhttpheaders();

&openpage('SWE 3.2 Credits'."$title", 1, , 'about your smoothie');
&openbigbox('100%', 'LEFT');
&alertbox($errormessage);

&openbox("SWE Credits:");

print <<END
<div style="margin:1.5em auto; width:95%; max-height:400px; overflow:auto">
<p>Smoothwall Express 3.2 would not have been possible without the hard work of many individuals, either directly or indirectly. Listed here are some of those individuals who either directly contributed to the codebase or who authored mods that have been integrated:</p>
<table class='list'>
<tr>
	<th class='list' style='width: 15%;'>Name</th>
	<th class='list' style='width: 10%;'>Forum Link</th>
	<th class='list' style='width: 40%;'>Contribution (if specified)</th>
	<th class='list' style='width: 5%;'></th>
</tr>
<tr><td>Alasak</td><td></td><td>Original author of Smoothwall</td></tr>
<tr><td>Fest3er</td><td></td><td>SWE Team Lead and Principle Developer</td></tr>
<tr><td>ShorTie</td><td></td><td>Author/Maintainer of RPi/ARM port and updated many packages, 3.2 was based off of his work.</td></tr>
<tr><td>S-T-P</td><td></td><td>Author of integrated FFC mod</td></tr>
<tr><td>Wkitty42</td><td></td><td>Author of integrated GAR mod</td></tr>
<tr><td>Dataking</td><td></td><td>Author of integrated Advanced Firewall Stats mod, groundwork for htop integration</td></tr>
<tr><td>Panda</td><td></td><td>Author of integrated SSDtrim mod</td></tr>
<tr><td>Guypat</td><td></td><td>Author of Whatmasks mod</td></tr>
<tr><td>RobertWillett</td><td></td><td>Author of improved graphs.cgi</td></tr>
<tr><td>JohnH</td><td></td><td>Author of integrated performance graphs mod</td></tr>

END
;

print "</table></div>";

&closebox();

print "<br />\n";
print "</div>";

&closebox();
&closebox();

&alertbox('add','add');
&closebigbox();
&closepage();
