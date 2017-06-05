#!/usr/bin/perl
use warnings;
use strict;
use FindBin qw($RealBin);
use CGI;
use HTML::Template;
use lib "$RealBin/../packages";
use compter::Constants;

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

    $template -> param(
	MAX_DATA_SIZE => $compter::Constants::MAX_DATA_SIZE,
	COMPTER_VERSION => $compter::Constants::COMPTER_VERSION,
	ADMIN_EMAIL => $compter::Constants::ADMIN_EMAIL,
	

	);


    print $template->output();
					 


}
