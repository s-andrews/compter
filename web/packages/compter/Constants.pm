#!/usr/bin/perl
use warnings;
use strict;
use FindBin;

package compter::Constants;

our $COMPTER_VERSION = `$FindBin::RealBin/../../compter --version`;

# The constants below are populated from a file called
# sierra.conf in the conf directory of your sierra
# installation.  You should not edit any of the values in
# this file, but should use the conf file to alter the
# values stored in this package.

our $BASE_URL;
our $DATA_DIR;
our $MAX_DATA_SIZE;
our $RETENTION_TIME;
our $ADMIN_NAME;
our $ADMIN_EMAIL;
our $SMTP_SERVER;
our $SMTP_USERNAME;
our $SMTP_PASSWORD;
our $MAILS_FROM_ADDRESS;
our $R_PATH;

parse_conf_file ();

sub parse_conf_file {

  unless (-e "$FindBin::RealBin/../conf/compterweb.conf") {
    die "No compterweb.conf file found in $FindBin::RealBin/../conf/ - copy the example conf file and set the values up for your installation";
  }

  open (CONF,"$FindBin::RealBin/../conf/compterweb.conf") or die "Can't open compterweb.conf file: $!";

  while (<CONF>) {
    chomp;
    next unless ($_);

    next if (/^\s*\#/); # Ignore comments

    my ($name,$value) = split(/\s+/,$_,2);

    if ($name eq 'BASE_URL') {
      $BASE_URL = $value;
    }

    elsif ($name eq 'DATA_DIR') {
      unless (-e $value and -d $value) {
	die "Temp folder '$value' doesn't exist";
      }
      $DATA_DIR = $value;
    }
    elsif ($name eq 'MAX_DATA_SIZE') {
      $MAX_DATA_SIZE = $value;
      unless ($MAX_DATA_SIZE =~ /^\d+$/) {
	  die "MAX_DATA_SIZE must be an integer, not '$MAX_DATA_SIZE'";
      }
    }
    elsif ($name eq 'RETENTION_TIME') {
      $RETENTION_TIME = $value;
      unless ($RETENTION_TIME =~ /^\d+$/) {
	  die "RETENTION_TIME must be an integer, not '$RETENTION_TIME'";
      }
    }
    elsif ($name eq 'ADMIN_NAME') {
      $ADMIN_NAME = $value;
    }
    elsif ($name eq 'ADMIN_EMAIL') {
      $ADMIN_EMAIL = $value;
    }
    elsif ($name eq 'SMTP_SERVER') {
      $SMTP_SERVER = $value;
    }
    elsif ($name eq 'SMTP_USERNAME') {
      $SMTP_USERNAME = $value;
    }
    elsif ($name eq 'SMTP_PASSWORD') {
      $SMTP_PASSWORD = $value;
    }
    elsif ($name eq 'MAILS_FROM_ADDRESS') {
      $MAILS_FROM_ADDRESS = $value;
    }
    elsif ($name eq 'R_PATH') {
      $R_PATH = $value;
    }
    else {
      close CONF;
      die "Unknown configuration otion '$name'";
    }
  }

  close CONF;

}


1;

