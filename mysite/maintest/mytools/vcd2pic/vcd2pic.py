import re
from PIL import Image, ImageDraw, ImageFont


def vcd2pic(vcd_location, pic_location):
    with open(vcd_location) as vcd:
        input = []
        output = []
        for each_line in vcd:

            word=each_line.strip().split()
            if not word:
                continue
            print(word)
            if word[0]=='$date':
                date=vcd.readline()
                #print(date)
            if word[0]=='$version':
                version=vcd.readline()
                #print(version)
            if word[0]=='$timescale':
                timescale=vcd.readline()
                timescale_value=re.search(r'\d',timescale).group()
                timescale_scale=re.search(r'[a-z]{1,2}',timescale).group()
                '''
                print(timescale)
                print(timescale_value)
                print(timescale_scale)
                '''
            if word[0]=='$scope':
                module_name=word[2]
                #print(module_name)
            if word[0]=='$var':
                if word[1]=="reg":
                    input.append({'name':word[4],'sign':word[3],'timescale':word[2],'wave':[],'state':[]})
                if word[1]=="wire":
                    output.append({'name':word[4],'sign':word[3],'timescale':word[2],'wave':[],'state':[]})
            line=each_line
            while re.search(r'^#',line):
                time=re.search(r'\d{1,3}',line).group()
                line = vcd.readline()
                if line=='$dumpvars\n':
                    waveout = input + output
                    line=vcd.readline()
                for i in range(len(waveout)):
                    if int(time) != 0:
                        temp_list = waveout[i]['wave']
                        waveout[i]['wave'].append(temp_list[-1])
                while (re.search(r'^\d',line)):
                    sign=re.search(r'\d\W',line)
                    for i in range(len(waveout)):
                        if sign.group()[1]==waveout[i]['sign']:
                            if int(time) == 0:
                                waveout[i]['wave'].append(sign.group()[0])
                            else:
                                waveout[i]['wave'][-1]=sign.group()[0]
                    line=vcd.readline()
                if line=='$end\n':
                    line = vcd.readline()
                    continue
    for i in range(len(waveout)):
        for j in range(len(waveout[i]['wave'])):
            if j==0:
                waveout[i]['state'].append(0)
            else:
                b_wave=int(waveout[i]['wave'][j-1])
                now_wave=int(waveout[i]['wave'][j])
                if b_wave==0 and now_wave==0:
                    waveout[i]['state'].append(0)
                if b_wave==0 and now_wave==1:
                    waveout[i]['state'].append(1)
                if b_wave==1 and now_wave==1:
                    waveout[i]['state'].append(2)
                if b_wave==1 and now_wave==0:
                    waveout[i]['state'].append(3)

    green = (0, 255, 0)
    tint_green = (0, 80, 0)
    tint_write = (255, 255, 255)

    unit_width = 40
    width = unit_width * (int(time)+3)
    unit_height = 20
    height = unit_height * (len(waveout)+1)

    image = Image.new('RGB', (width, height), (0, 0, 0))

    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype('arial.ttf', 12)

    def zero_zero(begin_width, begin_height, unit_width, unit_height):
        for x in range(begin_width, begin_width + unit_width):
            draw.point((x, begin_height + unit_height-1), fill=green)

    def zero_one(begin_width, begin_height, unit_width, unit_height):
        for x in range(begin_width, begin_width + unit_width):
            if x == begin_width:
                for y in range(begin_height + int(0.2 * unit_height), begin_height + unit_height):
                    draw.point((x, y), fill=green)
            else:
                for y in range(begin_height + int(0.2 * unit_height), begin_height + unit_height):
                    if y > begin_height + int(0.2 * unit_height):
                        draw.point((x, y), fill=tint_green)
                    elif y == begin_height + int(0.2 * unit_height):
                        draw.point((x, y), fill=green)

    def one_zero(begin_width, begin_height, unit_width, unit_height):
        for x in range(begin_width, begin_width + unit_width):
            if x == begin_width:
                for y in range(begin_height + int(0.2 * unit_height), begin_height + unit_height):
                    draw.point((x, y), fill=green)
            else:
                draw.point((x, begin_height + unit_height - 1), fill=green)

    def one_one(begin_width, begin_height, unit_width, unit_height):
        for x in range(begin_width, begin_width + unit_width):
            for y in range(begin_height + int(0.2 * unit_height), begin_height + unit_height):
                if y > begin_height + int(0.2 * unit_height):
                    draw.point((x, y), fill=tint_green)
                elif y == begin_height + int(0.2 * unit_height):
                    draw.point((x, y), fill=green)

    def draw_time(begin_width, begin_height, unit_width, unit_height,time):
        for x in range(begin_width,begin_width+unit_width):
            if x == begin_width:
                for y in range(begin_height+int(unit_height * 0.6), begin_height+unit_height):
                    draw.point((x, y), fill=tint_write)
            elif x == begin_width+unit_width / 2:
                for y in range(begin_height+int(unit_height * 0.85),begin_height+unit_height):
                    draw.point((x, y), fill=tint_write)
            else:
                draw.point((x,begin_height+unit_height - 1), fill=tint_write)
        draw.text((begin_width,begin_height), text='%d'%i+'us', font=font, fill=tint_write)

    def draw_name(begin_width, begin_height, unit_width, unit_height,name):
        draw.text((begin_width+unit_width / 4,begin_height+unit_height / 10), text=name, font=font, fill=tint_write)
    for i in range(int(time)+1):
        draw_time((i+2)*unit_width,0, unit_width, unit_height, i)
    for i in range(len(waveout)+1):
        if i==0:
            draw_name(0,i*unit_height, unit_width, unit_height,"name")
        else:
            draw_name(0,i * unit_height, unit_width, unit_height, waveout[i-1]["name"])
    for i in range(len(waveout)):
        for j in range(len(waveout[i]['state'])):
            if waveout[i]['state'][j] == 0:
                zero_zero((j+2) * unit_width, (i+1) * unit_height,unit_width,unit_height)
            elif waveout[i]['state'][j] == 1:
                zero_one((j+2) * unit_width, (i+1) * unit_height,unit_width,unit_height)
            elif waveout[i]['state'][j] == 2:
                one_one((j+2) * unit_width, (i+1) * unit_height,unit_width,unit_height)
            elif waveout[i]['state'][j] == 3:
                one_zero((j+2) * unit_width, (i+1) * unit_height,unit_width,unit_height)
    image.show()
    image.save(pic_location, 'jpeg')


if __name__ == '__main__':
    vcd2pic('test_tri.vcd','wave.jpg')