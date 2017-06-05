#!/usr/bin/perl
use warnings;
use strict;
use FindBin qw($RealBin);
use CGI;
use HTML::Template;
use lib "$RealBin/../packages";
use compter::Constants;
use CGI::Carp qw(fatalsToBrowser);

my $q = CGI -> new();


my $job_id = $q->param("job_id");

if ($job_id) {
    show_job($job_id);
}
else {
    show_upload();
}


sub show_job {

    my ($job_id) = @_;

}



sub show_upload {

    my $template = HTML::Template -> new(filename => "$RealBin/../templates/submission.html");

    # We need to get a list of the available background
    # species on this machine
    my @species;

    open (SPECIES, "$RealBin/../../compter --bglist 2>&1 |") or die "Can't get background species list";

    while (<SPECIES>) {
	next if (/^Backgrounds/);
	next if (/^----/);

	chomp;
	s/^\s+//g;
	next unless ($_);
	push @species, {SPECIES_NAME => $_};
    }

    close SPECIES;


    $template -> param(
	MAX_DATA_SIZE => $compter::Constants::MAX_DATA_SIZE,
	COMPTER_VERSION => $compter::Constants::COMPTER_VERSION,
	ADMIN_EMAIL => $compter::Constants::ADMIN_EMAIL,
	SPECIES => \@species,

	);


    print $template->output();
					 


}
