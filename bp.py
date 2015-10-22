#!/usr/bin/python  
# -*- coding=UTF8 -*-  

import os
import time
from optparse import OptionParser

blogdir="/home/hexo/blog/"
srcdir=blogdir+"source/_posts/"
outdir=blogdir+"source/assets/backup/"
linkdir=blogdir+"source/link/"
pnglink="/assets/backup/"
splitstr="\n\n\n\nsstask\n\n\n\n"

rsrc=outdir
rdst="/home/hexo/blog/myblog/

def genfile(fn):
    print "genfile %s" % (fn)
    outf = outdir+os.path.basename(fn)+".png"
    os.system("qrencode -o %s \"%s\"" % (outf,fn))#生成二维码
    fp = open(outf,"ab+")
    fp.writelines(splitstr)#分隔符
    fp1 = open(fn,"rb")
    fp.writelines(fp1.read(os.path.getsize(fn)))
    fp1.close()
    fp.close()

    fi=open(linkdir+"index.md","a")#写到link文件中
    fi.write("![%s](%s)\n" % (os.path.basename(fn),pnglink+os.path.basename(fn)+".png"))
    fi.close()
    return

def genblog():
    print "generate blog"
    os.system("hexo g")
    print "deploy blog"
    os.system("hexo d")
    return

def backup():
    print "begin ..."
    if os.path.exists(srcdir)==False:
        print "no blog"
        return
    if os.path.exists(outdir)==False:
        os.makedirs(outdir)
    if os.path.exists(linkdir)==False:
        os.makedirs(linkdir)
    if os.path.exists(linkdir+"index.md")==True:
        os.remove(linkdir+"index.md")
    fi=open(linkdir+"index.md","w")
    fi.writelines("title: link\ndate: %s\n---\n" % (time.strftime("%Y-%m-%d %X",time.localtime())))
    fi.close() 
    for parent,dirnames,filenames in os.walk(srcdir):
        for filename in filenames:
            genfile(parent+filename)
    genblog()
    return

def refile(fn):
    fp = open(fn,"rb")
    content=fp.read(os.path.getsize(fn))
    fp.close()
    pos=content.find(splitstr)
    if pos >= 0:
        print "revert file %s" % (fn)
        ct=content[pos+len(splitstr):]
        fname=os.path.basename(fn)
        fname=fname[0:-4]
        fi=open(rdst+fname,"w")
        fi.writelines(ct)
        fi.close()
    return

def revert():
    if os.path.exists(rsrc)==False:
        print "no backup file"
        return
    if os.path.exists(rdst)==False:
        os.makedirs(rdst)
    for parent,dirnames,filenames in os.walk(rsrc):
        for filename in filenames:
            refile(parent+filename)
    return

def main():  
    try:  
        usage = "usage: %prog [options] arg"
        parser = OptionParser(usage)
        (options, args) = parser.parse_args()
        if len(args) > 0:
            if args[0] == "b":
                backup()
            elif args[0] == "r":
                revert()
            else:
                print "error arg"
        else:
            print "need arg"
    except KeyboardInterrupt:  
        print "用户中断"  
    except Exception, e:  
        print e  
  
    return  
  
if __name__ == "__main__":  
    main() 
