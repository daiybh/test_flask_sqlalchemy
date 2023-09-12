# convert 123.lsprj  to json
# read file (123.lsprj) 
# parse it to json save to file (123.json)

# the 123.lsprj is a xml file 
import json
import xmltodict


def convert_file_to_json(file_path):
    with open(file_path, 'r',encoding='utf-8') as file:
        data = file.read()

    json_data = xmltodict.parse(data)

    return json_data


from PIL import Image, ImageDraw, ImageFont

def drawBackImage(json_data):
    ledJson= json_data["LEDS"]["LED"]

    ledWidth=int(ledJson['@LedWidth'])
    ledHeight=int(ledJson['@LedHeight'])

    areas= ledJson['Program']['Area']

    image = Image.new("RGB", (ledWidth, ledHeight), (0, 0, 0))
    draw = ImageDraw.Draw(image)

    for area in areas:
        areaLeft=int(area['@AreaRect_Left'])
        areaTop=int(area['@AreaRect_Top'])
        areaRight=int(area['@AreaRect_Right'])-1
        areaBottom=int(area['@AreaRect_Bottom'])

        draw.rectangle((areaLeft, areaTop,areaRight, areaBottom),outline='red',width=1)
    
    return image
        
def drawJson(json_data,showText):    
    ledJson= json_data["LEDS"]["LED"]

    ledWidth=int(ledJson['@LedWidth'])
    ledHeight=int(ledJson['@LedHeight'])

    areas= ledJson['Program']['Area']

    image = Image.new("RGB", (ledWidth, ledHeight), (0, 0, 0))
    draw = ImageDraw.Draw(image)

    for area in areas:
        areaName=area['@AreaName']
        areaNo=int(area['@AreaNo'])-1
        areaLeft=int(area['@AreaRect_Left'])
        areaTop=int(area['@AreaRect_Top'])
        areaRight=int(area['@AreaRect_Right'])
        areaBottom=int(area['@AreaRect_Bottom'])
        IsUsreBorder=area['@IsUseBorder']
        borderColor = area['@BorderColor']

        if 'SingleLineArea' not in area:
            continue

        rtfText = area['SingleLineArea']['#text']
        #parseRTF(rtfText)
        print(areaName)
        text_color=(255,0,0)
        font = ImageFont.truetype("simsun.ttc", 30)
        text_position=areaLeft,areaTop
        areaWidth= areaRight - areaLeft
        areaHeight= areaBottom - areaTop

        if IsUsreBorder=="1":
            draw.rectangle((areaLeft, areaTop,areaRight, areaBottom),outline='red',width=2)
            text_position=areaLeft+2,areaTop+2
        
        text = f"{areaName}:{IsUsreBorder}"
        text=""
        if areaNo < len(showText):
            text = showText[areaNo]['F_message']
        
        text_width, text_height = font.getsize(text)
        text_position = ((areaWidth - text_width) // 2, ((areaHeight - text_height) // 2)+areaTop)
        draw.text(text_position,text,font=font, fill=text_color)

    #image.save('123.png')
    return image



def genrate_image(lsprj,showText,pngSavePathPrex):
    a = convert_file_to_json(lsprj)

    showGroup={}
    for i in range(0,len(showText)):
        key = str(int(i/4))
        if key not in showGroup:
            showGroup[key] = []
        showGroup[ key].append(showText[i])

    result=[]
    for key in showGroup:
        image_a = drawJson(a,showGroup[key])
        pngPath= f"{pngSavePathPrex}_{key}.png"
        image_a.save(pngPath)
        result.append(pngPath)
    return result

def generate_backImage(lsprj,pngSavePath):
    a = convert_file_to_json(lsprj)
    image_a = drawBackImage(a)
    image_a.save(pngSavePath)
    return pngSavePath
    

    

if __name__=="__main__":
    #genrate_image("123.lsprj",["第一行 1235","456","789","abc","B123"])#,"B456","B789","Babc"])

    generate_backImage("C:\\Users\\yg\\Desktop\\a\\123.lsprj","123.png")