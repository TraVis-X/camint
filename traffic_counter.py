import motion_detector
count = 0
def main():
    s = input('Do you want to detect using camera or videofile?:(0/1)')
    if s=='0':
        count = motion_detector.detect(int(s))
    else:
        count = motion_detector.detect('motion2.mp4')
    print("Number of vehicles %(count)d" % {"count":count})

if __name__=='__main__':
    main()
