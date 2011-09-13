#!/usr/local/strategic/perl/bin/perl
use 5.14.1;
use warnings;
use FindBin;
use Template;
use CGI;
use DateTime;

eval {
    my $cgi = CGI->new;

    my %date = decode_date($cgi->param('date'));
    my %time = decode_time($cgi->param('time'));

    my $dt = DateTime->new( %date, %time );

    my $future = DateTime->from_epoch(
        epoch => $dt->epoch + 10e8
    );

    header('text/html');
    output(birthday => $dt, birthsecond => $future);
};
if ($@) {
    header('text/plain');
    say "Error: $@";
    exit;
}

sub header {
    my $content = shift || 'text/html';
    say "Content-type: $content";
    say 'Cache-control: no-cache';
    say '';
}

sub decode_date {
    my $date_str = shift;
    given ($date_str) {
        when (/^\s*(\d{4})\-(\d{1,2})\-(\d{1,2})\s*$/) {
            return(
                year => $1,
                month => $2,
                day => $3,
            )
        }
        when (/^\s*(\d{1,2})[-\\\/](\d{1,2})[-\\\/](\d{4})\s*$/) {
            return(
                day => $1,
                month => $2,
                year => $3,
            )
        }
        default {
            die "Could not understand date format.\n"
        }
    }
}

sub decode_time {
    my $time_str = shift;
    given ($time_str) {
        when (/^\s*(\d{1,2}):(\d\d)\s*$/) {
            return( hour => $1, minute => $2 )
        }
        default {
            die "Could not understand time format.\n"
        }
    }
}

# ghetto style templating :(
sub output {
    my %vars = @_;

    $vars{datedisplay} = sub {
        my $dt = shift;
        return join(' ',
            $dt->month_name, $dt->day, $dt->year,
            'at', $dt->hms
        );
    };

    my $tt = Template->new(
        {
            INCLUDE_PATH => "$FindBin::Bin/templates"
        }
    );
    $tt->process('birthsecond.tt', \%vars);
}
