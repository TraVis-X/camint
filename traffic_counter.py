import motion_detector

def main():
    s = input('Do you want to detect using camera or videofile?:(0/1)')
    if s=='0':
        motion_detector.detect(int(s))
    else:
        motion_detector.detect('motion2.mp4')

if __name__=='__main__':
    main()
