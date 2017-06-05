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
$CGI::POST_MAX=2*1024*$compter::Constants::MAX_DATA_SIZE;

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

    # Get the first fastq file
    my $fastq1 = $q -> param("fastq1");

    unless($fastq1) {
	print_error("First fastq file was not supplied");
	return;
    }

    # We'll remove leading and trailing slashes
    $fastq1 =~ s/^.*\///;
    $fastq1 =~ s/^.*\\//;
    

    my $fastq2 = $q->param("fastq2");
    # Fastq2 is optional so it's not a problem if it's not there

    if ($fastq2) {
	$fastq2 =~ s/^.*\///;
	$fastq2 =~ s/^.*\\//;
    }


    my $bgtype = $q ->param("background");
    my $gc;
    my $species;

    if ($bgtype eq "none") {
	$bgtype = "none";
    }
    elsif ($bgtype eq 'theoretical') {
	# We need to get the %gc value
	
	$gc = $q -> param("percentgc");

	unless ($gc and $gc =~ /^\d+$/) {
	    print_error("GC value '$gc' was not an integer when defining a theoretical background");
	    return;
	}

	if ($gc < 1 or $gc > 99) {
	    print_error("GC value must be in the range 1-99, (yours was $gc)");
	}
    }
    elsif ($bgtype eq 'precalc') {
	$species = $q->param("precalc_species");

	unless ($species) {
	    die "No species provides for precalculated background";
	}

    }
    else {
	die "Couldn't find a valid bgtype (got '$bgtype'";
    }

    # Now we can make a data folder
    my ($code,$dir) = make_run_dir();

    chdir($dir) or die "Failed to move to $dir: $!";

    # We can now write out the sequence data into the new folder
    my $fh1 = $q -> upload("fastq1");

    open (FQ1,">","$fastq1") or die "Can't write to $fastq1: $!";

    binmode FQ1;
    binmode $fh1;
    

    print FQ1 while (<$fh1>);

    close $fh1;
    close FQ1 or die "Can't complete write to $fastq1: $!";

    if ($fastq2) {
	my $fh2 = $q -> upload("fastq2");

	open (FQ2,">","$fastq2") or die "Can't write to $fastq2: $!";

	binmode FQ2;
	binmode $fh2;
    

	print FQ2 while (<$fh2>);

	close $fh2;
	close FQ2 or die "Can't complete write to $fastq2: $!";

    }


    # We can now constuct the compter command

    my $compter_command = "$RealBin/../../compter";

    # Add the background

    # Specify the data

    $compter_command .= " \"$fastq1\"";
    $compter_command .= " \"$fastq2\"" if ($fastq2);
    
    # Redirect the output
    $compter_command .= " > compter_log.txt 2>compter_errors.txt";

    # Run the command
    `$compter_command`;

    # Send them to the progress page for the job
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
