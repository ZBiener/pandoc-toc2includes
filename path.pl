#!/usr/bin/env perl

use strict;
use warnings;
use File::Find;

my @filelist = [];

sub process_file {
    # do whatever;
    if ($File::Find::name =~ /(.*)\.md/) {
        push(@filelist, $File::Find::name);
    }
}
find(\&process_file, qw(.));
print @filelist;