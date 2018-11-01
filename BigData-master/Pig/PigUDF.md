
#students.dat
abc,56,600117
cdr,67,600118
erf,88,600123
adc,76,600117
cddr,97,600118
cdf,28,600123
abec,86,600117
cdfrr,97,600118
erwwf,08,600123
adwwc,66,600117
cwdr,37,600118
cwfede,68,600123
ceabc,26,600117
cdcedr,37,600118
erefcef,84,600123
adecc,16,600117
cdddecr,37,600118
cdeddcf,78,600123
abedec,16,600117


#myudf.py
@outputSchema("record: {(rank:int, name:chararray, gpa:double, zipcode:chararray)}")
def enumerate_bag(input):
    output = []
    for rank, item in enumerate(input):
        output.append(tuple([rank] + list(item)))
    return output


register 'myudf.py' using jython as myudf;
students = load 'students.dat' using PigStorage(',') as (name:chararray, gpa:double, zipcode:chararray);
students_by_zipcode = group students by zipcode;
result = foreach students_by_zipcode {
           sorted = order students by gpa desc;
           ranked = myudf.enumerate_bag(sorted);
           generate flatten(ranked);
        };
dump result;