#!/usr/bin/perl
use warnings;
use strict;
use FindBin qw($RealBin);
use CGI;
use HTML::Template;

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

    print $template->output();
					 


}
