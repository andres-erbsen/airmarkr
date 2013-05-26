#!/usr/bin/env python3
# Written by Andres Erbsen and Sandra Schumann, distributed under the GNU GPLv3

from sys import argv, stdout

def sfloat(s):
    try:
        return float(s)
    except ValueError:
        return s

def buttonEvents(dat_file_contents):
    buttonlines = (l for l in dat_file_contents.splitlines() if l.startswith('Button'))
    return [(float(t)/1000000000, e) for (e,t) in map(str.split,buttonlines)]

def csvTrace(dat_file_contents, rtslam_log_contents):
    button = list(reversed(sorted(buttonEvents(dat_file_contents))))
    trace = (
        list(map(sfloat,l.split()))
        for l in rtslam_log_contents.splitlines()
        if l.strip() and not l.strip().startswith('#')
    )
    ret = []
    for tup in trace:
        t,_,x,y,z = tup[:5]
        buttonevent = 0
        while button and t > button[-1][0]:
            if button.pop()[1] == 'Buttondown':
                 buttonevent = 1
            else:
                 buttonevent = 2
        ret.append( (x,y,z,round(t*1000),buttonevent) )
    return '\n'.join("%f %f %f %d %d" % t for t in ret) + '\n'

if __name__ == "__main__":
    stdout.write( csvTrace( open(argv[1]).read(), open(argv[2]).read() ) )
