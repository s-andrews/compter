#!/usr/bin/perl
use warnings;
use strict;
use FindBin qw($RealBin);
use CGI;
use HTML::Template;
use lib "$RealBin/../packages";
use compter::Constants;
use CGI::Carp qw(fatalsToBrowser);


# This sets the maximum POST size.  In the conf file
# the value they set is the size per file so we double
# that and convert to bytes to set this value correctly.
$CGI::POS_MAX=2*1024*$compter::Constants::MAX_DATA_SIZE;

my $q = CGI -> new();


my $job_id = $q->param("job_id");

if ($job_id) {
    show_job($job_id);
}
elsif ($q->param("submit")) {
    process_submission();
}
else {
    show_upload();
}


sub show_job {

    my ($job_id) = @_;

    die "Showing details for $job_id";

}


sub process_submission {



    my ($code,$dir) = make_run_dir();

    print $q->redirect("$compter::Constants::BASE_URL?job_id=$code");


}


sub make_run_dir {

    # This sub creates a new run folder in the directory specified
    # by DATA_DIR and returns the code and the full path


    my $tries = 0;

    my @letters = ("a".."z","A".."Z",0..9);

    while ($tries <= 10) {
	++$tries;
	my $code;
	for (1..20) {
	    $code .= $letters[int(rand(@letters))];
	}

	# Check if this exists
	my $path = "$compter::Constants::DATA_DIR/$code";

	if (-e $path) {
	    next;
	}

	# Try to make it
	mkdir($path) or die "Can't make path $path: $!";

	# It worked
	return ($code,$path);

    }

    die "Failed to create run folder, even after 10 tries";

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
