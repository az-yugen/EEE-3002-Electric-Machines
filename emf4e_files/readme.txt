This archive contains electronic files to accompany "Electric 
Machinery Fundamentals", fourth edition, by Stephen J. Chapman.  
It contains the m-files used to generate examples in the book, 
plus electronic versions of the magnetization curves used in end-
of-chapter exercises.  It should be unpacked with an unzip 
program that preserves long file names, such as WinZip. 

Many of the problems in Chapters 2, 5, 6, and 9 require that a 
student read one or more values from a magnetization curve.  The 
required curves are given within the textbook, but they are shown 
with relatively few vertical and horizontal lines so that they 
will not appear too cluttered.  Electronic copies of the 
corresponding open-circuit characteristics, short-circuit 
characteristics, and magnetization curves are supplied in this 
archive.  They are supplied as ASCII text files.  Students can 
use these files for electronic solutions to homework problems.

The ASCII files have the file name "xxx_occ.dat" for AC machine open-
circuit characteristics (open-circuit terminal voltage versus 
field current), "xxx_scc.dat" for AC machine short-circuit 
characteristics (short-circuit line current versus field 
current), "xxx_ag_occ.dat" for AC machine unsaturated open-circuit 
characteristics (unsaturated open-circuit terminal voltage versus 
field current), and "xxx_mag.dat" for other magnetization curves.   
Each file contains a header that describes the two quantities 
contained in the file, and where appropriate, the speed of 
rotation at which the data was taken.  

Each curve is given in ASCII format with comments at the beginning. 
For example, the magnetization curve in Figure P9-1 is contained 
in file p91_mag.dat.  Its contents are shown below:

% This is the magnetization curve shown in Figure 
% P9-1.  The first column is the field current in
% amps, and the second column is the internal 
% generated voltage in volts at a speed of 1200 r/min.
% To use this file in MATLAB, type "load p91_mag.dat".  
% The data will be loaded into an N x 2 array named
% "p91_mag", with the first column containing If and 
% the second column containing the open-circuit voltage.
% MATLAB function "interp1" can be used to recover
% a value from this curve.
       0        0
  0.0132     6.67
    0.03    13.33
   0.033       16
   0.067    31.30
     0.1    45.46
   0.133    60.26
   0.167    75.06
     0.2    89.74
   0.233    104.4
   0.267   118.86
     0.3   132.86
   0.333   146.46
   0.367   159.78
     0.4   172.18
   0.433   183.98
   0.467   195.04
     0.5   205.18
   0.533   214.52
   0.567   223.06
     0.6    231.2
   0.633      238
   0.667   244.14
     0.7   249.74
   0.733   255.08
   0.767    259.2
     0.8   263.74
   0.833    267.6
   0.867    270.8
     0.9    273.6
   0.933   276.14
   0.966      278
       1   279.74
   1.033   281.48
   1.067   282.94
     1.1   284.28
   1.133   285.48
   1.167   286.54
     1.2    287.3
   1.233   287.86
   1.267   288.36
     1.3   288.82
   1.333    289.2
   1.367  289.375
     1.4  289.567
   1.433  289.689
   1.466  289.811
     1.5  289.950

To use this curve in a MATLAB program, the user would include 
the following statements in the program:

% Get the magnetization curve.  Note that this curve is
% defined for a speed of 1200 r/min.
load p91_mag.dat
if_values = p91_mag(:,1);
ea_values = p91_mag(:,2);
n_0 = 1200;

Then, arrays if_values and ea_values could be used to interpolate
any desired point along the curve.
