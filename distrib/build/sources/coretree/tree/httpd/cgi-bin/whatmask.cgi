#!/usr/bin/perl
#
# SmoothWall CGIs
#
# This code is distributed under the terms of the GPL
#
# (c) The SmoothWall Team

use lib "/usr/lib/smoothwall";
use header qw( :standard );

my %DETAILS;
&readhash("/var/smoothwall/mods/whatmask/DETAILS", \%DETAILS);

my %cgiparams;
my (@addrs, my @vars);
my $addr;
my $var;
my $infomessage = '';
my $errormessage = '';
use strict;
use warnings;

&getcgihash(\%cgiparams);
&showhttpheaders();

sub strim { 
	my $s = shift; 
	$s =~ s/\s//g;
	return $s 
};

if ($ENV{'QUERY_STRING'} && $cgiparams{'ACTION'} eq '') {
	@vars = split(/\&/, $ENV{'QUERY_STRING'});
	$cgiparams{'IP'} = '';
	foreach $_ (@vars) {
		($var, $addr) = split(/\=/);
		if ($var eq 'ip') {
			$cgiparams{'IP'} .= "$addr,";
			push(@addrs, $addr);
		} elsif ( $var eq "MODE" ) {
			$cgiparams{'MODE'} = $addr;
		}
        }
        $cgiparams{'ACTION'} = 'Run';
} else {
	@addrs = split(/,/, $cgiparams{'IP'});
}

foreach $addr (@addrs) {
	if (!&validipormask(strim($addr))) {
		$errormessage .= $tr{'invalid ip'} ."<br />";
		last;
	}
}

if ( $cgiparams{'MODE'} ne "weird" ) {
	&openpage($tr{'whatmask'}, 1, '', 'tools');
	&openbigbox('100%', 'LEFT');
	&alertbox($errormessage, "", $infomessage);

	print "<FORM METHOD='POST'>\n";
	&openbox($tr{'whatmask'});
	print <<END
<TABLE WIDTH='100%'>
	<TR>
		<TD WIDTH='25%' CLASS='base'>$tr{'whatmask-ip'}</TD>
		<TD WIDTH='40%'><INPUT TYPE='hidden' id='whatmask' name='whatmask' value='whatmask'><INPUT TYPE='text' SIZE='40' NAME='IP' VALUE='$cgiparams{'IP'}'></TD>
		<TD WIDTH='10%' ALIGN='CENTER'><INPUT TYPE='submit' NAME='ACTION' VALUE='$tr{'run'}'></TD>
	</TR>
</TABLE>
END
;
	&closebox();

	if ($cgiparams{'ACTION'} eq $tr{'run'} && $cgiparams{'whatmask'} eq 'whatmask') {
		@addrs = split(/,/, strim($cgiparams{'IP'}));
		foreach $addr (@addrs) {
			if (&validipormask($addr)) {
				&openbox("${addr}");
				print "<PRE>\n";
					system("/var/smoothwall/mods/whatmask/bin/whatmask", $addr);
				print "</PRE>";
				&closebox();
		}	}
	} 
	print "</FORM>\n";
}

print "<div style='float:right'><a href='$DETAILS{'MOD_FORUM'}' title='$tr{'whatmask-Go to the SW Forums'} $DETAILS{'MOD_NAME'} $tr{'whatmask-Mod thread'}.'> $DETAILS{'MOD_NAME'} $DETAILS{'MOD_VERSION'}&nbsp;</a></div>";
&alertbox('add','add');
&closebigbox();
&closepage();
