#!/usr/bin/perl
#
# SmoothWall CGIs
#
# This code is distributed under the terms of the GPL
#
# (c) The SmoothWall Team

use lib "/usr/lib/smoothwall";
use header qw( :standard );
use smoothtype qw(:standard);

my %cgiparams;
my $filename = "${swroot}/vpn/config";

$cgiparams{'ENABLED'} = 'off';
$cgiparams{'COMPRESSION'} = 'off';
&getcgihash(\%cgiparams);

my $errormessage = '';

if ($cgiparams{'ACTION'} eq $tr{'add'})
{
	unless ($cgiparams{'NAME'} =~ /^[a-zA-Z]+$/) {
		$errormessage = $tr{'name must only contain characters'}; }
	unless (&validip($cgiparams{'LEFT'})) { 
		$errormessage = $tr{'left ip is invalid'}; }
	unless (&validipandmask($cgiparams{'LEFT_SUBNET'})) {
		$errormessage = $tr{'left subnet is invalid'}; }
	unless (&validip($cgiparams{'RIGHT'})) { 
		$errormessage = $tr{'right ip is invalid'}; }
	unless (&validipandmask($cgiparams{'RIGHT_SUBNET'})) {
		$errormessage = $tr{'right subnet is invalid'}; }

	unless ( &validcomment( $cgiparams{'COMMENT'} ) ){ $errormessage = $tr{'invalid comment'};  }

	unless ($timesettings{'SECRET1'} and ($timesettings{'SECRET1'} =~ /^[\w\d\.\-,\(\)@$!\%\^\&\*=\+_ ]*$/ )) {
		$errormessage = $tr{'bad password'};
	}

	unless ($timesettings{'SECRET2'} and ($timesettings{'SECRET2'} =~ /^[\w\d\.\-,\(\)@$!\%\^\&\*=\+_ ]*$/ )) {
		$errormessage = $tr{'bad password'};
	}

	if ($cgiparams{'SECRET1'} ne $cgiparams{'SECRET2'}) {
		$errormessage = $tr{'passwords do not match'}; }
	unless ($cgiparams{'SECRET1'}) {
		$errormessage = $tr{'password not set'}; } 
	open(FILE, $filename) or die 'Unable to open config file.';
	my @current = <FILE>;
	close(FILE);
	unless ($errormessage)
	{
		open(FILE,">>$filename") or die 'Unable to open config file.';
		flock FILE, 2;
		print FILE "$cgiparams{'NAME'},$cgiparams{'LEFT'},$cgiparams{'LEFT_SUBNET'},$cgiparams{'RIGHT'},$cgiparams{'RIGHT_SUBNET'},$cgiparams{'SECRET1'},$cgiparams{'ENABLED'},$cgiparams{'COMPRESSION'},$cgiparams{'COMMENT'}\n";
		close(FILE);
		undef %cgiparams;

		system('/usr/bin/smoothwall/writeipsec.pl');
	}
}
if ($cgiparams{'ACTION'} eq $tr{'remove'} || $cgiparams{'ACTION'} eq $tr{'edit'})
{
	open(FILE, "$filename") or die 'Unable to open config file.';
	my @current = <FILE>;
	close(FILE);

	my $count = 0;
	my $id = 0;
	my $line;
	foreach $line (@current)
	{
		$id++;
		if ($cgiparams{$id} eq "on") {
			$count++; }
	}
	if ($count == 0) {
		$errormessage = $tr{'nothing selected'}; }
	if ($count > 1 && $cgiparams{'ACTION'} eq $tr{'edit'}) {
		$errormessage = $tr{'you can only select one item to edit'}; }
	unless ($errormessage)
	{
		open(FILE, ">$filename") or die 'Unable to open config file.';
		flock FILE, 2;
		my $id = 0;
		foreach $line (@current)
		{
			$id++;
			unless ($cgiparams{$id} eq "on") {
				print FILE "$line"; }
			elsif ($cgiparams{'ACTION'} eq $tr{'edit'})
			{
				chomp($line);
				my @temp = split(/\,/,$line);
				$cgiparams{'NAME'} = $temp[0];
				$cgiparams{'LEFT'} = $temp[1];
				$cgiparams{'LEFT_SUBNET'} = $temp[2];
				$cgiparams{'RIGHT'} = $temp[3];
				$cgiparams{'RIGHT_SUBNET'} = $temp[4];
				$cgiparams{'SECRET1'} = $temp[5];
				$cgiparams{'SECRET2'} = $temp[5];
				$cgiparams{'ENABLED'} = $temp[6];
				$cgiparams{'COMPRESSION'} = $temp[7];
				$cgiparams{'COMMENT'} = $temp[8];
			}
		}
		close(FILE);

		system('/usr/bin/smoothwall/writeipsec.pl');
	}
}
if ($cgiparams{'ACTION'} eq $tr{'export'})
{
	print "Content-type: unknown/unknown\n\n";
	open (FILE, "$filename");
	my @current = <FILE>;
	close (FILE);
	print @current;
	exit;
}
if ($cgiparams{'ACTION'} eq $tr{'import'})
{
        if (length($cgiparams{'FH'}) > 1)
	{
                open(FILE, ">$filename") or $errormessage = 
			'Could not open config file for writing';
		flock FILE, 2;
		binmode(FILE);
                print FILE $cgiparams{'FH'};
		close (FILE);
		
		system('/usr/bin/smoothwall/writeipsec.pl');
	}
}
if ($cgiparams{'ACTION'} eq '')
{
        $cgiparams{'ENABLED'} = 'on';
	$cgiparams{'COMPRESSION'} = 'off';
}

my %checked;
$checked{'ENABLED'}{'off'} = '';
$checked{'ENABLED'}{'on'} = '';
$checked{'ENABLED'}{$cgiparams{'ENABLED'}} = 'CHECKED';

$checked{'COMPRESSION'}{'off'} = '';
$checked{'COMPRESSION'}{'on'} = '';
$checked{'COMPRESSION'}{$cgiparams{'COMPRESSION'}} = 'CHECKED';

&showhttpheaders();

&openpage('VPN configuration - Connections', 1, '', 'vpn');

&openbigbox();

&alertbox($errormessage);

print "<FORM METHOD='POST'>\n";

&openbox($tr{'add a new connection'});
print <<END
<TABLE WIDTH='100%'>
<TR>
<TD WIDTH='25%' CLASS='base'>$tr{'namec'}</TD>
<TD WIDTH='25%'><INPUT TYPE='TEXT' NAME='NAME' VALUE='$cgiparams{'NAME'}' id='name' @{[jsvalidregex('name','^[a-zA-Z]+$')]}></TD>
<TD class='base' WIDTH='25%'>Compression:</tD>
<TD WIDTH='25%'><INPUT TYPE='CHECKBOX' NAME='COMPRESSION' $checked{'COMPRESSION'}{'on'}></TD>
<TR>
<TD CLASS='base'>$tr{'leftc'}</TD>
<TD><INPUT TYPE=TEXT NAME='LEFT' VALUE='$cgiparams{'LEFT'}' id='left' @{[jsvalidip('left')]}></TD>
<TD CLASS='base'>$tr{'left subnetc'}</TD>
<TD><INPUT TYPE=TEXT NAME='LEFT_SUBNET' VALUE='$cgiparams{'LEFT_SUBNET'}' id='left_subnet' @{[jsvalidipandmask('left_subnet')]}></TD>
</TR>
<TR>
<TD CLASS='base'>$tr{'rightc'}</TD>
<TD><INPUT TYPE=TEXT NAME='RIGHT' VALUE='$cgiparams{'RIGHT'}' id='right' @{[jsvalidip('right')]} ></TD>
<TD CLASS='base'>$tr{'right subnetc'}</TD>
<TD><INPUT TYPE=TEXT NAME='RIGHT_SUBNET' VALUE='$cgiparams{'RIGHT_SUBNET'}' id='right_subnet' @{[jsvalidipandmask('right_subnet')]}></TD>
</TR>
<TR>
<TD CLASS='base'>$tr{'secretc'}</TD>
<TD COLSPAN='4'>
<INPUT TYPE='PASSWORD' NAME='SECRET1' VALUE='$cgiparams{'SECRET1'}' SIZE='40' id='secret1' @{[jsvalidpassword('secret1','secret2',,'^[a-zA-Z0-9\.,\(\)@$!\%\^\&\*=\+_ ]*$')]}></TD>
</TR>
<TR>
<TD CLASS='base'>$tr{'again'}</TD>
<TD COLSPAN='4'>
<INPUT TYPE='PASSWORD' NAME='SECRET2' VALUE='$cgiparams{'SECRET2'}' SIZE='40' id='secret2' @{[jsvalidpassword('secret2','secret1','^[a-zA-Z0-9\.,\(\)@$!\%\^\&\*=\+_ ]*$')]} ></TD>
</TR>
<tr>
	<td class='base'>$tr{'commentc'}</td>
	<td colspan='3'><input type='text' style='width: 80%;' name='COMMENT' value='$cgiparams{'COMMENT'}' id='comment' @{[jsvalidcomment('comment')]}  ></td>
</tr>
</TABLE>
<TABLE WIDTH='100%'>
<TR>
<TD class='base' WIDTH='25%'>$tr{'enabled'}</TD>
<TD WIDTH='25%'><INPUT TYPE='CHECKBOX' NAME='ENABLED' $checked{'ENABLED'}{'on'}></TD>
<TD WIDTH='50%' colspan='2' ALIGN='CENTER'><INPUT TYPE='SUBMIT' NAME='ACTION' VALUE='$tr{'add'}'></TD>
</TR>
</TABLE>
END
;
&closebox();

&openbox($tr{'current connections'});

print "<table class='centered'>\n";

my $id = 0;
open(RULES, "$filename") or die 'Unable to open config file.';
while (<RULES>)
{
	my $egif; my $cgif;
	$id++;
	chomp($_);
	my @temp = split(/\,/,$_);
	my $class;
	if ($id % 2) {
		$class = 'light'; }
	else {
		$class = 'dark'; }
 	if ($temp[6] eq 'on') { $egif = 'on.gif'; }
                else { $egif = 'off.gif'; }
 	if ($temp[7] eq 'on') { $cgif = 'on.gif'; }
                else { $cgif = 'off.gif'; }
print <<END
<tr class='$class'>
<td style='width: 25%;'><strong>$tr{'namec'}</strong> $temp[0]</td>
<td style='width: 25%;'><strong>$tr{'enabled'} </strong><img src='/ui/img/$egif'></td>
<td style='width: 25%;'><strong>Compression: </strong><img src='/ui/img/$cgif'></td>
<td style='width: 25%;'>&nbsp;</td>
</tr>
<tr class='$class'>
<td><strong>$tr{'leftc'}</strong> $temp[1]</td>
<td><strong>$tr{'left subnetc'}</strong> $temp[2]</td>
<td><strong>$tr{'rightc'} </strong>$temp[3]</td>
<td><strong>$tr{'right subnetc'} </strong>$temp[4]</td>
</tr>
<tr class='$class'>
<td colspan='3'><strong>$tr{'commentc'}</strong> $temp[8]</td>
<td><strong>$tr{'markc'} </strong><input type='checkbox' name='$id'></td>
</tr>
END
	;
}
close(RULES);

print <<END
</table>
<table class='blank'>
<tr>
<td style='text-align: center;'><input type='submit' name='ACTION' value='$tr{'remove'}'></td>
<td style='text-align: center;'><input type='submit' name='ACTION' value='$tr{'edit'}'></td>
</tr>
</table>
END
;
&closebox();

&openbox($tr{'import and export'});
print <<END
<DIV ALIGN='CENTER'>
<TABLE WIDTH='80%'>
<TR>
<TD ALIGN='LEFT'><INPUT TYPE='SUBMIT' NAME='ACTION' VALUE='$tr{'export'}'></TD>
</FORM>
<FORM METHOD='POST' ENCTYPE='multipart/form-data'>
<TD ALIGN='RIGHT'><INPUT TYPE='FILE' NAME='FH' SIZE='30'>
<INPUT TYPE='SUBMIT' NAME='ACTION' VALUE='$tr{'import'}'></TD>
</FORM>
</TR>
</TABLE>
</DIV>
END
;
&closebox();

&alertbox('add','add');

&closebigbox();

&closepage();
