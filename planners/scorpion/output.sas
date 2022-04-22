begin_version
3
end_version
begin_metric
0
end_metric
4
begin_variable
var0
-1
7
Atom current(hospital)
Atom current(l2)
Atom current(l3)
Atom current(l4)
Atom current(l5)
Atom current(l6)
Atom current(l7)
end_variable
begin_variable
var1
-1
2
Atom free(ambulance)
NegatedAtom free(ambulance)
end_variable
begin_variable
var2
-1
8
Atom at(patient1, hospital)
Atom at(patient1, l2)
Atom at(patient1, l3)
Atom at(patient1, l4)
Atom at(patient1, l5)
Atom at(patient1, l6)
Atom at(patient1, l7)
Atom carry(patient1, ambulance)
end_variable
begin_variable
var3
-1
8
Atom at(patient2, hospital)
Atom at(patient2, l2)
Atom at(patient2, l3)
Atom at(patient2, l4)
Atom at(patient2, l5)
Atom at(patient2, l6)
Atom at(patient2, l7)
Atom carry(patient2, ambulance)
end_variable
1
begin_mutex_group
3
2 7
3 7
1 0
end_mutex_group
begin_state
0
0
4
5
end_state
begin_goal
2
2 0
3 0
end_goal
38
begin_operator
getinto patient1 hospital ambulance
1
0 0
2
0 2 0 7
0 1 0 1
1
end_operator
begin_operator
getinto patient1 l2 ambulance
1
0 1
2
0 2 1 7
0 1 0 1
1
end_operator
begin_operator
getinto patient1 l3 ambulance
1
0 2
2
0 2 2 7
0 1 0 1
1
end_operator
begin_operator
getinto patient1 l4 ambulance
1
0 3
2
0 2 3 7
0 1 0 1
1
end_operator
begin_operator
getinto patient1 l5 ambulance
1
0 4
2
0 2 4 7
0 1 0 1
1
end_operator
begin_operator
getinto patient1 l6 ambulance
1
0 5
2
0 2 5 7
0 1 0 1
1
end_operator
begin_operator
getinto patient1 l7 ambulance
1
0 6
2
0 2 6 7
0 1 0 1
1
end_operator
begin_operator
getinto patient2 hospital ambulance
1
0 0
2
0 3 0 7
0 1 0 1
1
end_operator
begin_operator
getinto patient2 l2 ambulance
1
0 1
2
0 3 1 7
0 1 0 1
1
end_operator
begin_operator
getinto patient2 l3 ambulance
1
0 2
2
0 3 2 7
0 1 0 1
1
end_operator
begin_operator
getinto patient2 l4 ambulance
1
0 3
2
0 3 3 7
0 1 0 1
1
end_operator
begin_operator
getinto patient2 l5 ambulance
1
0 4
2
0 3 4 7
0 1 0 1
1
end_operator
begin_operator
getinto patient2 l6 ambulance
1
0 5
2
0 3 5 7
0 1 0 1
1
end_operator
begin_operator
getinto patient2 l7 ambulance
1
0 6
2
0 3 6 7
0 1 0 1
1
end_operator
begin_operator
getout patient1 hospital ambulance
1
0 0
2
0 2 7 0
0 1 -1 0
1
end_operator
begin_operator
getout patient1 l2 ambulance
1
0 1
2
0 2 7 1
0 1 -1 0
1
end_operator
begin_operator
getout patient1 l3 ambulance
1
0 2
2
0 2 7 2
0 1 -1 0
1
end_operator
begin_operator
getout patient1 l4 ambulance
1
0 3
2
0 2 7 3
0 1 -1 0
1
end_operator
begin_operator
getout patient1 l5 ambulance
1
0 4
2
0 2 7 4
0 1 -1 0
1
end_operator
begin_operator
getout patient1 l6 ambulance
1
0 5
2
0 2 7 5
0 1 -1 0
1
end_operator
begin_operator
getout patient1 l7 ambulance
1
0 6
2
0 2 7 6
0 1 -1 0
1
end_operator
begin_operator
getout patient2 hospital ambulance
1
0 0
2
0 3 7 0
0 1 -1 0
1
end_operator
begin_operator
getout patient2 l2 ambulance
1
0 1
2
0 3 7 1
0 1 -1 0
1
end_operator
begin_operator
getout patient2 l3 ambulance
1
0 2
2
0 3 7 2
0 1 -1 0
1
end_operator
begin_operator
getout patient2 l4 ambulance
1
0 3
2
0 3 7 3
0 1 -1 0
1
end_operator
begin_operator
getout patient2 l5 ambulance
1
0 4
2
0 3 7 4
0 1 -1 0
1
end_operator
begin_operator
getout patient2 l6 ambulance
1
0 5
2
0 3 7 5
0 1 -1 0
1
end_operator
begin_operator
getout patient2 l7 ambulance
1
0 6
2
0 3 7 6
0 1 -1 0
1
end_operator
begin_operator
move hospital l2
0
1
0 0 0 1
1
end_operator
begin_operator
move l2 hospital
0
1
0 0 1 0
1
end_operator
begin_operator
move l2 l3
0
1
0 0 1 2
1
end_operator
begin_operator
move l2 l4
0
1
0 0 1 3
1
end_operator
begin_operator
move l2 l5
0
1
0 0 1 4
1
end_operator
begin_operator
move l3 l2
0
1
0 0 2 1
1
end_operator
begin_operator
move l4 l6
0
1
0 0 3 5
1
end_operator
begin_operator
move l5 l7
0
1
0 0 4 6
1
end_operator
begin_operator
move l6 l3
0
1
0 0 5 2
1
end_operator
begin_operator
move l7 l3
0
1
0 0 6 2
1
end_operator
0
begin_SG
switch 0
check 0
switch 1
check 1
28
switch 2
check 0
check 1
0
check 0
check 0
check 0
check 0
check 0
check 0
check 0
switch 3
check 0
check 1
7
check 0
check 0
check 0
check 0
check 0
check 0
check 0
check 0
check 0
switch 2
check 0
check 0
check 0
check 0
check 0
check 0
check 0
check 0
check 1
14
switch 3
check 0
check 0
check 0
check 0
check 0
check 0
check 0
check 0
check 1
21
check 0
switch 1
check 4
29
30
31
32
switch 2
check 0
check 0
check 1
1
check 0
check 0
check 0
check 0
check 0
check 0
switch 3
check 0
check 0
check 1
8
check 0
check 0
check 0
check 0
check 0
check 0
check 0
check 0
switch 2
check 0
check 0
check 0
check 0
check 0
check 0
check 0
check 0
check 1
15
switch 3
check 0
check 0
check 0
check 0
check 0
check 0
check 0
check 0
check 1
22
check 0
switch 1
check 1
33
switch 2
check 0
check 0
check 0
check 1
2
check 0
check 0
check 0
check 0
check 0
switch 3
check 0
check 0
check 0
check 1
9
check 0
check 0
check 0
check 0
check 0
check 0
check 0
switch 2
check 0
check 0
check 0
check 0
check 0
check 0
check 0
check 0
check 1
16
switch 3
check 0
check 0
check 0
check 0
check 0
check 0
check 0
check 0
check 1
23
check 0
switch 1
check 1
34
switch 2
check 0
check 0
check 0
check 0
check 1
3
check 0
check 0
check 0
check 0
switch 3
check 0
check 0
check 0
check 0
check 1
10
check 0
check 0
check 0
check 0
check 0
check 0
switch 2
check 0
check 0
check 0
check 0
check 0
check 0
check 0
check 0
check 1
17
switch 3
check 0
check 0
check 0
check 0
check 0
check 0
check 0
check 0
check 1
24
check 0
switch 1
check 1
35
switch 2
check 0
check 0
check 0
check 0
check 0
check 1
4
check 0
check 0
check 0
switch 3
check 0
check 0
check 0
check 0
check 0
check 1
11
check 0
check 0
check 0
check 0
check 0
switch 2
check 0
check 0
check 0
check 0
check 0
check 0
check 0
check 0
check 1
18
switch 3
check 0
check 0
check 0
check 0
check 0
check 0
check 0
check 0
check 1
25
check 0
switch 1
check 1
36
switch 2
check 0
check 0
check 0
check 0
check 0
check 0
check 1
5
check 0
check 0
switch 3
check 0
check 0
check 0
check 0
check 0
check 0
check 1
12
check 0
check 0
check 0
check 0
switch 2
check 0
check 0
check 0
check 0
check 0
check 0
check 0
check 0
check 1
19
switch 3
check 0
check 0
check 0
check 0
check 0
check 0
check 0
check 0
check 1
26
check 0
switch 1
check 1
37
switch 2
check 0
check 0
check 0
check 0
check 0
check 0
check 0
check 1
6
check 0
switch 3
check 0
check 0
check 0
check 0
check 0
check 0
check 0
check 1
13
check 0
check 0
check 0
switch 2
check 0
check 0
check 0
check 0
check 0
check 0
check 0
check 0
check 1
20
switch 3
check 0
check 0
check 0
check 0
check 0
check 0
check 0
check 0
check 1
27
check 0
check 0
end_SG
begin_DTG
1
1
28
0
4
0
29
0
2
30
0
3
31
0
4
32
0
1
1
33
0
1
5
34
0
1
6
35
0
1
2
36
0
1
2
37
0
end_DTG
begin_DTG
14
1
0
2
0 0
2 0
1
1
2
0 1
2 1
1
2
2
0 2
2 2
1
3
2
0 3
2 3
1
4
2
0 4
2 4
1
5
2
0 5
2 5
1
6
2
0 6
2 6
1
7
2
0 0
3 0
1
8
2
0 1
3 1
1
9
2
0 2
3 2
1
10
2
0 3
3 3
1
11
2
0 4
3 4
1
12
2
0 5
3 5
1
13
2
0 6
3 6
14
0
14
2
0 0
2 7
0
15
2
0 1
2 7
0
16
2
0 2
2 7
0
17
2
0 3
2 7
0
18
2
0 4
2 7
0
19
2
0 5
2 7
0
20
2
0 6
2 7
0
21
2
0 0
3 7
0
22
2
0 1
3 7
0
23
2
0 2
3 7
0
24
2
0 3
3 7
0
25
2
0 4
3 7
0
26
2
0 5
3 7
0
27
2
0 6
3 7
end_DTG
begin_DTG
1
7
0
2
0 0
1 0
1
7
1
2
0 1
1 0
1
7
2
2
0 2
1 0
1
7
3
2
0 3
1 0
1
7
4
2
0 4
1 0
1
7
5
2
0 5
1 0
1
7
6
2
0 6
1 0
7
0
14
1
0 0
1
15
1
0 1
2
16
1
0 2
3
17
1
0 3
4
18
1
0 4
5
19
1
0 5
6
20
1
0 6
end_DTG
begin_DTG
1
7
7
2
0 0
1 0
1
7
8
2
0 1
1 0
1
7
9
2
0 2
1 0
1
7
10
2
0 3
1 0
1
7
11
2
0 4
1 0
1
7
12
2
0 5
1 0
1
7
13
2
0 6
1 0
7
0
21
1
0 0
1
22
1
0 1
2
23
1
0 2
3
24
1
0 3
4
25
1
0 4
5
26
1
0 5
6
27
1
0 6
end_DTG
begin_CG
3
1 28
2 14
3 14
2
2 7
3 7
1
1 14
1
1 14
end_CG
