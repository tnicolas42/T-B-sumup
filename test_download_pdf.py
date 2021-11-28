# https://gist.github.com/Spencer-Easton/78f9867a691e549c9c70

# format=xlsx       # excel
# format=ods        # Open Document Spreadsheet
# format=zip        # html zipped          

# CSV,TSV OPTIONS***********
# format=csv        #  comma seperated values
#              tsv        #  tab seperated values
# gid=sheetId             #  the sheetID you want to export, The first sheet will be 0. others will have a uniqe ID

#  PDF OPTIONS****************
# format=pdf     
# size=0,1,2..10             paper size. 0=letter, 1=tabloid, 2=Legal, 3=statement, 4=executive, 5=folio, 6=A3, 7=A4, 8=A5, 9=B4, 10=B5  
# fzr=true/false             repeat row headers
# portrait=true/false        false =  landscape
# fitw=true/false            fit window or actual size
# gridlines=true/false
# printtitle=true/false
# pagenum=CENTER/UNDEFINED      CENTER = show page numbers / UNDEFINED = do not show
# attachment = true/false      dunno? Leave this as true
# gid=sheetId                 Sheet Id if you want a specific sheet. The first sheet will be 0. others will have a uniqe ID. 
                            #  Leave this off for all sheets. 
#  EXPORT RANGE OPTIONS FOR PDF
# need all the below to export a range
# gid=sheetId                must be included. The first sheet will be 0. others will have a uniqe ID
# ir=false                   seems to be always false
# ic=false                   same as ir
# r1=Start Row number - 1        row 1 would be 0 , row 15 wold be 14
# c1=Start Column number - 1     column 1 would be 0, column 8 would be 7   
# r2=End Row number
# c2=End Column number

file_id = "1ZRQtumM4RETSOQUSOoCnGGDKtAZVVC1zv2y0eA2LFY4"

def get_link(file_id):
    return "https://docs.google.com/spreadsheets/d/" + file_id + "/export" + \
        "?format=pdf" + \
        "&size=7" + \
        "&portrait=true" + \
        "&gridlines=false" + \
        "&gid=1169815886"

print(get_link(file_id=file_id))