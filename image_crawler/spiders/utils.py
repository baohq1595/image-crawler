
shape_mapping = {1: 'other', 2: 'spoke', 3: 'dish', 4: 'mesh'}
color_mapping = {2: 'silver', 4: 'chrome', 6: 'gunmetal',
                7: 'gold', 8: 'white', 9: 'black',
                10: 'bronze', 11: 'polish', 12: 'titanium',
                13: 'pink', 14: 'yellow', 15: 'green',
                16: 'red', 17: 'blue', 1: 'other'}

color_marker = 'wc='
shape_marker = 'wd='

def generate_query_urls():
    urls = []
    # 'https://www.maluzen.com/wheelcatalog/?pg=3&wd=4&wz=&wc=2&wb=&wm=&wma=&wyo=&_=1568279481404'
    for skey, svalue in shape_mapping.items():
        for ckey, cvalue in color_mapping.items():
            urls.append(
                'https://www.maluzen.com/wheelcatalog/?wd={}&wz=&wc={}&wb=&wm=&wma=&wyo='.\
                    format(skey, ckey)
            )
    
    return urls

def get_image_attrs(url: str):
    shape = 'other'
    color = 'other'
    shape_pos = url.find(shape_marker)
    color_pos = url.find(color_marker)
    if shape_pos != -1:
        marked_pos = shape_pos + len(shape_marker) 
        shape = shape_mapping.get(
            int(url[marked_pos:marked_pos + 1]), 'other'
        )
    
    if color_pos != -1:
        marked_pos = color_pos + len(color_marker)
        color = color_mapping.get(
            int(url[marked_pos:marked_pos + 1]), 'other'
        )

    shape_id = 1
    color_id = 1
    for key, value in shape_mapping.items():
        if value == shape:
            shape_id = key
    
    for key, value in color_mapping.items():
        if value == shape:
            color_id = key

    return shape_id, color_id