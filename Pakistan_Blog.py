import requests
import numpy as np
import panel as pn
import folium
import ipyleaflet
from collections import defaultdict



# Panel-Erweiterung und Schriftart einbinden ----Philipp---
pn.extension(
    raw_css=[
        """
        /* Google Fonts Import */
        @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@300;400;700&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@400;500;700&display=swap');

        
        /* Globale Schriftart auf Nunito setzen */
        body {
            font-family: 'Quicksand', sans-serif;
        }

        /*Quicksand als Überschriftschrift*/
        h1, h2, h3, h4, h5, h6 {
            font-family: 'Quicksand', sans-serif;
        }

        
        /* Runde Ecken und Begrenzung des Inhalts für Matplotlib-Canvas */
        .canvas-container {
            border-radius: 15px; /* Runde Ecken */
            overflow: hidden;    /* Begrenzung des Inhalts */
            background: white;   /* Hintergrundfarbe */
            padding: 0px;        /* Kein Platzverlust im Inneren */
            margin: 15px;        /* Zusätzlicher Abstand nach außen */
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1); /* Optional: Schatten */
        }

        /* Runde Ecken und Begrenzung des Inhalts für Matplotlib-Canvas */
        .canvas-container-logo {
            border-radius: 10px; /* Runde Ecken */
            overflow: hidden;    /* Begrenzung des Inhalts */
            background: white;   /* Hintergrundfarbe */
            padding: 0px;        /* Kein Platzverlust im Inneren */
            margin: 0px;        /* Zusätzlicher Abstand nach außen */
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1); /* Optional: Schatten */
        }
        /* Runde Ecken für PNG-Bilder */
        .bk.pane img {
            border-radius: 15px;
        }

       /* Runde Ecken und Schatten für alle Panele */
        .rounded-panel {
            border-radius: 10px;
            background: #F3F4F6;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
        }
        
        /* Runde Ecken und Schatten für navigation elements */
        .navigation-panel {
            border-radius: 10px;
            background: #9C978E;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
        }


        /* Runde Ecken für Buttons */
        .rounded-button {
            border-radius: 15px;
        }
        """
    ]
)

#----------------------------------------------------------

m = folium.Map(location=[30.70, 73.05], zoom_start=6,attr="<a href=https://api.maptiler.com//>maptiler</a>",tiles="https://api.maptiler.com/maps/basic-v2/{z}/{x}/{y}.png?key=tlMO9QKlWXNxmYv2hETr")

#folium.Marker([64.03947, -22.69782], popup="<i>1.Tag Sandgerði</i>", tooltip="Click me!").add_to(m)


color_code={"site_color": "green",
        "uni_color": "blue",
        "hotel_color": "red"}

# Dictionary to store markers by day
days = defaultdict(lambda: None)

# Read data from file

#https://raw.githubusercontent.com/Koppeprojects/Pakistan_blog/refs/heads/main/markers.txt
url="https://raw.githubusercontent.com/Koppeprojects/Pakistan_blog/refs/heads/main/markers.txt"
response = requests.get(url)
if response.status_code == 200:
    file = response.text
    #print(file)  # Print first 500 characters
else:
    print("Failed to load file")
lines = file.split("\n")

#with open("https://raw.githubusercontent.com/Koppeprojects/Pakistan_blog/refs/heads/main/markers.txt", "r") as file:
for line in lines:
    print(line)
    parts = line.strip().split(",")  # Split by comma
    if len(parts) == 5:
        day, lat, lon, popup, coded_color = parts
        lat, lon = float(lat), float(lon)  # Convert coordinates
        # Create a feature group for each day if not already created
        if day not in days:
            days[day] = folium.FeatureGroup(name=day).add_to(m)
        
        # Add marker to the respective day's feature group
        folium.Marker(
            [lat, lon],
            popup=f"<i>{popup}</i>",
            tooltip="Click me!",
            icon=folium.Icon(color_code[coded_color])  # Change icon color as needed
        ).add_to(days[day])

#day1 = folium.FeatureGroup("1. Tag").add_to(m)

#folium.Marker([64.03947, -22.69782], popup="<i> Campingplatz Sandgerði</i>", tooltip="Click me!",icon=folium.Icon(site_color)).add_to(day1)

folium.LayerControl().add_to(m)

folium_pane = pn.pane.plot.Folium(m, height=1000)

#Beispiel
#p1 = pn.pane.Markdown("""
#
#<img src="https://github.com/Koppeprojects/Islandbilder/blob/main/bildertag1/unendliche_weite.jpeg?raw=true" alt="weite" width="800" />
#
#Angekommen in Island suchen wir am Flughafen,
# [Campingcard](https://utilegukortid.is/?lang=de) hier 
#
#
#---
#
#Schafcounter:42
#
#Wetterbeschreibung: 10&deg;C viel wolkig ein bisschen Sprüregen
#
#Hotpot max. Temperatur: -
#
#
#""")


days_pn = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

for i in range(22):
    #https://raw.githubusercontent.com/Koppeprojects/Pakistan_blog/refs/heads/main/days/day0.txt
    dateiname="https://raw.githubusercontent.com/Koppeprojects/Pakistan_blog/refs/heads/main/days/day"+str(i)+".txt"
    print("Es wird untersucht der Tag",i)
    try:
        response = requests.get(dateiname)
        if response.status_code == 200:
            dateicontent = response.text
            #print(content[:500])  # Print first 500 characters
        else:
            print("Failed to load file")
        #with open(dateiname, "r", encoding='utf-8') as f:
        #    dateicontent= f.read()
        #print(dateicontent)
        if dateicontent=="":
            print("nothing inside")
        else:
            print("it is something inside")
            days_pn[i]=pn.pane.Markdown(dateicontent)       
    except:
        print(dateiname)
        print("Day not yet exists")








#Physikstudent-Content
#with open("html/Physikstudent-content.html", "r", encoding='utf-8') as f:
#    sphy_content= f.read()

#escaped_sphy = html.escape(sphy_content) #scrolling=no style="height:100%; width:100%" style="width:75vw; height:90vh"
#iframe_sphy = f'<iframe srcdoc="{escaped_sphy}" style="height:100%; width:100%"  frameborder="0"></iframe>'    


# Status-Flag für die Farbe des Navigationsbuttons
status = {"Karte": "success"} # entries detemine the color.... success light warning 
for i in range(15):
    if days_pn[i]!=0:
        status["Tag "+str(i)] = "light"
    else:
        print("day not initialized")
if days_pn[20]!=0:
    status["Zusatz"] = "light"
else:
    print("day not initialized")


# Hauptfunktion für die Kalibrierungsseite
def create_card(page_name):
    
    #Aufbau Seite: 
    return pn.Column(
        pn.pane.Markdown("# Willkommen zur Karte"), 
        folium_pane,
        css_classes=["rounded-panel"],
        sizing_mode="stretch_width",
    )


def create_page(page_name):
    # Inhalt von Seite 1
    title = pn.pane.Markdown("# Willkommen zum Eintrag: "+str(page_name))
    day_number_str = np.char.lstrip(page_name, 'Tag ')  # Remove leading 'Tag '
    day_number = day_number_str.astype(int)  # Convert to integers
    return pn.Column(
        title,
        days_pn[day_number],
        css_classes=["rounded-panel"])

def create_zusatz(page_name):
    
    #Aufbau Seite: 
    return pn.Column(
        days_pn[20], 
        css_classes=["rounded-panel"],
        sizing_mode="stretch_width",
    )

   



# Router für Seiten
pages = {"Karte": create_card}
for i in range(15):
    if days_pn[i]!=0:
        pages["Tag "+str(i)] = create_page
    else:
        print("day not initialized")
if days_pn[20]!=0:
    pages["Zusatz"] = create_zusatz
else:
    print("day not initialized")

# Navigation
def update_sidebar():
    # Buttons dynamisch neu erstellen
    buttons = []
    for page_name in pages:
        button = pn.widgets.Button(
            name=page_name,
            button_type=status.get(page_name, "primary"),  # Farbe aus Status-Flag
            width=200,
            styles={"border-radius": "15px"},
        )
        button.on_click(lambda event, name=page_name: switch_page(name))  # Event für Seitenwechsel
        buttons.append(button)
    
    # Sidebar aktualisieren
    sidebar[:] = [
        pn.pane.Markdown("## Navigation", styles={"color": "white", "margin-bottom": "10px"}),
        *buttons,
    ]



# Funktion für Seitenwechsel
def switch_page(page_name):
    main_content[:] = [pages[page_name](page_name)]  # Wechsle zu neuer Seite
    
#---Layout----
header = pn.Row(
    pn.pane.Markdown("# Reise Blog Pakistan", styles={'color': 'white'}), #Header und Überschrift
    pn.Spacer(sizing_mode="stretch_width"),                                                                 
    pn.pane.Image("Bilder/Deutschlandflagge.png", height=80, align="end", css_classes=["canvas-container-logo"]),
    pn.pane.Image("Bilder/Pakistanflagge.png", height=80, align="end", css_classes=["canvas-container-logo"]),
    styles={'background': '#7D7972', 'padding': '10px'}, #Padding =abstand
    height=100,
    sizing_mode="stretch_both",
    css_classes=["rounded-panel"]
)

# Sidebar initialisieren
main_content = pn.Column(pages["Karte"]("Karte"), sizing_mode="stretch_both", css_classes=["rounded-panel"]) # styles={'background': '#F3F4F6'}
sidebar = pn.Column(styles={"padding": "15px"}, sizing_mode="stretch_height", css_classes=["navigation-panel"])
update_sidebar()  # Initiale Sidebar erstellen


layout = pn.Column(
    header,
    pn.Spacer(height=10),
    pn.Row(sidebar, pn.Spacer(width=10), main_content),
    height=3000#sizing_mode="scale_width"
)




layout.servable()
