#!/usr/bin/env perl

use strict;
use warnings;
use File::Find;
use Array::Utils qw(:all);

my $filename = $ARGV[0];
my @available_flist = ();
my @toc_flist = ();
my @file_contents = ();
my @new_file_contents = ();
my @remaining_flist = ();

sub find_all_markdown_files_in_directory_tree {
    if ($File::Find::name =~ /(.*)\.md/) {push(@available_flist, $File::Find::name)}
    #     #print $File::Find::name;
    #     foreach my $file (@toc_flist) {
    #         if ($file eq $File::Find::name) {
    #             print "file:", $file, " is " , $File::Find::name, "\n"; 
    #             push(@available_flist, $File::Find::name);
    #         }

        # if ( grep { $_ ne $File::Find::name} @toc_flist ) {
        #     print "file:", $File::Find::name, "\n";
        #     }
    # }
        #}
    # }
}

sub load_file_contents_to_memory {
    open(my $fh, '<:encoding(UTF-8)', $filename)
        or die "Could not open file '$filename' $!";
    while ( <$fh> ) {
        push @file_contents, $_;
    }
    close($fh);
}

sub separate_pandoc_portion {
    foreach my $row (@file_contents) {   # Read input from command-line into default variable $_
            push(@new_file_contents, $row); 
            if ($row =~ /Other excluded files/) {last}
    }
}

sub process_pandoc_portion {
    # lines with file names are processed, adding to array of already-seen files, and fixing file paths
    foreach my $row (@new_file_contents) {   
        if ($row =~ /^\s*([\+-])\s*([\.\/]*)(.*)(\.md)/) {
            push(@toc_flist, "\./$3$4");
            if ( $1 eq "+") {$row =~ s/\s*\+\s*(.*)(\.md)/{include=\"$1$2"}\n/;}
            elsif ( $1 eq "-" ) {$row =~ s/.*//g; chomp($row)} # throw away file
    # lines corresponding to headings are processed last
        } else {
        $row =~ s/---/---/;  # yaml line
        $row =~ s/^\+(.*)/#$1\n/;           #h1
        $row =~ s/^\s{2}\+(.*)/##$1\n/;     #h2
        $row =~ s/^\s{4}\+(.*)/###$1\n/;    #h3
        $row =~ s/^\s{6}\+(.*)/####$1\n/;   #h4
        } 
    # output to STDOUT pipe to pandoc
    #print "$row";
    }
}

sub find_files_in_directory_tree_but_not_pandoc_potion {
    my @remaining_flist = array_minus( @available_flist, @toc_flist );
}


sub write_file {
    open(my $fh, '>:encoding(UTF-8)', $filename)
        or die "Could not open file '$filename' $!";
    print $fh @new_file_contents;
    print $fh @remaining_flist;
    close($fh);

}

load_file_contents_to_memory();
separate_pandoc_portion();
process_pandoc_portion();
find(\&find_all_markdown_files_in_directory_tree, qw(.));
find_files_in_directory_tree_but_not_pandoc_potion();
write_file();

#print "TOCLIST:", @toc_flist;

