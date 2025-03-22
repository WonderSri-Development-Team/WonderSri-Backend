import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WonderSri_backend.settings')

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')

django.setup()

from tracking.models import MainGeofence, SubGeofence
from django.contrib.gis.geos import Polygon, Point

main_latlngs = [
    (80.213537, 6.030287),
    (80.213923, 6.026841),
    (80.217571,6.02379),          
    (80.219888,6.024526),
    (80.219964,6.027492),          
    (80.219159,6.029455),
    (80.217035,6.030853),
    (80.213537,6.030287),
]

main_polygon_obj = Polygon(main_latlngs)

galle_fort, created = MainGeofence.objects.get_or_create(
    name='Galle Fort',
    defaults={
        'location': main_polygon_obj,
        'description': """A UNESCO World Heritage Site, built by the Portuguese in 1588 and fortified by the Dutch in 1649.UNESCO World Heritage Site & Colonial Marvel
                        A 16th-century fortified city blending Portuguese, Dutch, and British architectural styles, Galle Fort is Sri Lanka's largest European-built fortress in Asia. Wander cobblestone streets lined with Dutch-era villas, colonial churches, and breezy verandas. 
                        Key highlights include the Galle Lighthouse (Sri Lanka's oldest), Dutch Hospital Shopping Precinct (now a chic dining hub), and Flag Rock Bastion (sunset views over the Indian Ocean).""",
        'main_point' : Point(80.21608, 6.030239, srid=4326)
    }
)
if created:
    print("New MainGeofence created:", galle_fort)
else:
    print("MainGeofence already exists:", galle_fort)

sub_geofences_data = [
    # name, polygon, description, main_point
    (
        "Galle Fort main entrance", 
        Polygon([
            (80.21601,6.030314),
            (80.216034,6.030002),
            (80.216176,6.030031),
            (80.216158,6.030341),
            (80.21601,6.030314)
        ]),
        """
        Historic Gateway to a UNESCO Treasure
        The Main Gate (also called the British Gate) is the northern entrance to Galle Fort, built by the British in 1873 to manage growing traffic into the fortified city. Located opposite the Galle International Cricket Stadium, this heavily fortified gateway reflects the fort's layered history:

         * Portuguese Origins: Initially fortified by the Portuguese in 1588 with a moat and bastions.

         * Dutch Reinforcement: Expanded by the Dutch in the 17th century with Star, Moon, and Sun Bastions to defend against land attacks.

         * British Era: The current gate's design prioritizes accessibility while retaining colonial charm.
        """,
        Point(80.21608, 6.030239, srid=4326)
    ),
    (
        "The Sun Bastion",
        Polygon([
            (80.216779, 6.030439),
            (80.216996, 6.030535),
            (80.216991, 6.030293),
            (80.216768, 6.030269),
            (80.216779, 6.030439)

        ]),
        """
        Dutch-Era Stronghold & Panoramic Vista
        A 17th-century Dutch fortification built to reinforce Galle Fort's northern defenses, the Sun Bastion (originally São Iago Bastion under the Portuguese) was renamed by the Dutch in 1667. Its strategic position allowed cannons to protect the harbor from inland attacks, with 15 cannons installed by 1760.

        Historic Layers: 
         * Portuguese Origins: Constructed in 1620 as part of the original fort.

         * Dutch Reinforcement: Strengthened with coral and granite to withstand sieges.

         * British Era: Later modified by the British, who added infrastructure like the Galle Lighthouse.
        """,
        Point(80.216812, 6.030274, srid=4326)
    ),
    (
        "Galle Clock Tower",
        Polygon([
            (80.215035, 6.030069),
            (80.215049, 6.029991),
            (80.215116, 6.030002),
            (80.215108, 6.030069),
            (80.215035, 6.030069)
        ]), 
        """
        Colonial Tribute & Timeless Landmark
        Built in 1883 to honor Dr. Peter Daniel Anthonisz, a pioneering Sri Lankan doctor, this British-era clock tower blends colonial architecture with local heritage. Standing 25 meters tall on the Moon Bastion, it features four clock faces visible across Galle Fort and a weathered stone exterior that reflects its resilience.

         * Historical Significance: Funded by public subscriptions to commemorate Dr. Anthonisz's contributions to public health.
                                    Designed by John Henry Gues Landon, with the clock donated by a grateful patient.

         * UNESCO Context: Part of Galle Fort, a UNESCO World Heritage Site recognized for its fusion of European and South Asian traditions.
        """,
        Point(80.215077, 6.029991, srid=4326)
    ),
    (
        "The Moon Bastion",
        Polygon([
            (80.215127, 6.030082),
            (80.214966, 6.030079),
            (80.214968, 6.030191),
            (80.215116, 6.030207),
            (80.215127, 6.030082)

        ]),
        """
        Dutch-Era Stronghold & Historical Hub
        A 17th-century Dutch bastion built to defend Galle Fort's northern flank, the Moon Bastion (originally São Iago Bastion under the Portuguese) was reconstructed by the Dutch in 1667 after their capture of the fort. Its strategic position allowed 16 cannons to protect against inland attacks, with the Galle Clock Tower later erected on its site in 1883.

         * Historical Layers:
                Portuguese Origins: Built in 1620 as part of the original fort.

                Dutch Reinforcement: Strengthened with coral and granite, housing 19 cannons by the late 17th century.

         * British Era: The Clock Tower dominates the bastion, funded by public subscriptions to honor Dr. Peter Daniel Anthonisz.

         * UNESCO Context:
                Part of Galle Fort, a UNESCO World Heritage Site recognized for its fusion of European and South Asian traditions.
        """,
        Point(80.215069, 6.030074, srid=4326)
    ),
    (
        "The Star Bastion",
        Polygon([
            (80.213633, 6.030223),
            (80.214043, 6.030127),
            (80.214054, 6.030005),
            (80.213633, 6.030063),
            (80.213633, 6.030223)
        ]),
        """
        Dutch-Era Coastal Defense & Strategic Stronghold
        A 17th-century Dutch bastion built to reinforce Galle Fort's southern defenses, the Star Bastion (originally constructed by the Portuguese in the 16th century) was strengthened by the Dutch in 1667 with coral and granite to protect against naval attacks. Its strategic position allowed six cannons to guard the harbor, ensuring the fort's role as a critical trading hub.

         * Historical Layers:
                Portuguese Origins: Built as part of the original fortifications in 1620.
                Dutch Reinforcement: Renamed Star Bastion in 1667 and fortified with six cannons to counter British and French threats.
                UNESCO Context: Part of Galle Fort, a UNESCO World Heritage Site recognized for its fusion of European and South Asian traditions.
        """,
        Point(80.213929, 6.030055, srid=4326)
    ),
    (
        "The Aeolus Bastion",
        Polygon([
        (80.213828, 6.02846),
        (80.213853, 6.028162),
        (80.213686, 6.02817),
        (80.213619, 6.028447),
        (80.213828, 6.02846)

        ]),
        """
        Dutch Naval Stronghold & Breezy Vantage Point
        A 17th-century Dutch bastion built to defend Galle Fort's western flank, the Aeolus Bastion (named after the Greek god of winds) was strategically positioned to harness sea breezes for Dutch naval ships. Part of a long rampart wall linking Sun Bastion to Flag Rock, it served as a gun platform and housed the Dutch Naval Commander's residence.

        Historical Context:

         * Dutch Era: Constructed in the 17th century as part of Galle Forts western defenses.

         * UNESCO Significance: Part of Galle Fort, a UNESCO World Heritage Site recognized for its fusion of European and South Asian traditions.
        """,
        Point(80.213867, 6.028364, srid=4326)
    ),
    (
        "The Clippenburg Bastion",
        Polygon([
            (6.027196, 80.214051),
            (6.026951, 80.214381),
            (6.026865, 80.213949),
            (6.027196, 80.214051)
        ]),
        """
        Dutch-Era Stronghold & Macabre History
        A 17th-century Dutch bastion built to reinforce Galle Fort's northern defenses, the Clippenburg Bastion (originally constructed in 1640) was rebuilt in 1752 with gravestones from Dutch cemeteries repurposed as flooring. Its strategic position allowed cannons to counter inland threats, while its crenellated walls and granite construction reflect Dutch engineering.

        Historical Layers:

         * Portuguese Origins: Part of the fort's early defenses, later fortified by the Dutch.

         * Dutch Reinforcement: Rebuilt in 1752 with gravestones from Dutch cemeteries, blending practicality with macabre reuse.

         * UNESCO Context: Part of Galle Fort, a UNESCO World Heritage Site recognized for its fusion of European and South Asian traditions.
        """,
        Point(80.214071, 6.027068, srid=4326)
    ),
    (
        "The Neptune Bastion",
        Polygon([
        (80.214748, 6.026516),
        (80.214612, 6.026438),
        (80.214622, 6.026201),
        (80.214944, 6.02631),
        (80.214748, 6.026516)

        ]),
        """
        WWII Signaling Hub & Coastal Defense
        A 17th-century Dutch gun platform on Galle Fort's western ramparts, Neptune Bastion later served as a British naval signaling tower during WWII to monitor enemy ships. Its strategic position allowed long-range cannon fire against maritime threats, with remnants of its flagstaff and signaling equipment still visible.

        Historical Layers:

         * Dutch Era: Built as part of the western rampart wall to defend against naval attacks.

         * British Era: Repurposed during WWII for naval surveillance and communication.

         * UNESCO Context: Part of Galle Fort, a UNESCO World Heritage Site recognized for its fusion of European and South Asian traditions.
        """,
        Point(80.214779, 6.026446, srid=4326)
    ),
    (
        "The Triton Bastion",
        Polygon([
        (80.216301, 6.025019),
        (80.216186, 6.024899),
        (80.215918, 6.024995),
        (80.216057, 6.025145),
        (80.216301, 6.025019)

        ]),
        """
        Dutch-Era Water Management & Colonial Ingenuity
        A 17th-century Dutch bastion built to reinforce Galle Forts western ramparts, Triton Bastion housed a windmill that pumped seawater into tanks to spray streets and keep the fort dust-free. Its strategic position compensated for weaknesses in the neighboring rampart, though it was too small to serve as a major defense platform.

        Historical Context:

         * Dutch Era: Constructed during Dutch rule (1640-1796) to support urban infrastructure.

         * UNESCO Significance: Part of Galle Fort, a UNESCO World Heritage Site recognized for its fusion of European and South Asian traditions.
        """,
        Point(80.216128, 6.025091, srid=4326)
    ),
    (
        "Flag Rock Bastion",
        Polygon([
        (80.21763, 6.023827),
        (80.217598, 6.023646),
        (80.21748, 6.023662),
        (80.217507, 6.023849),
        (80.21763, 6.023827)
        ]),
        """
        Colonial Watchtower & Sunset Spectacle
        Perched on the southernmost tip of Galle Fort, Flag Rock Bastion is a 17th-century Portuguese bastion later fortified by the Dutch to serve as a maritime signaling post. Its strategic position allowed the Dutch to hoist flags and fire musket shots from nearby Pigeon Island to warn ships of treacherous reefs. Today, it's a sunrise/sunset hotspot and a stage for local cliff divers.

        Historical Layers:

         * Portuguese Origins: Built in 1588 as part of Galle Fort's coastal defenses.

         * Dutch Reinforcement: Strengthened in the 17th century with cannons and a flag post to signal ships.

         * UNESCO Context: Part of Galle Fort, a UNESCO World Heritage Site recognized for its fusion of European and South Asian traditions.
        """,
        Point(80.21756, 6.023808, srid=4326)
    ),
    (
        "Galle Lighthouse", 
        Polygon([
            (80.219349,6.024571),
            (80.219465,6.024595),
            (80.219489,6.024496),
            (80.219339,6.024494),
            (80.219349,6.024571)
        ]), 
        """
        Sri Lankas Oldest Beacon & Colonial Legacy
        Standing 26.5 meters tall on Point Utrecht Bastion within Galle Fort (a UNESCO World Heritage Site), the Galle Lighthouse is Sri Lanka's oldest light station, guiding ships since the British rebuilt it in 1939 after a fire destroyed the original 1848 structure. Its strategic position offers panoramic views of the Indian Ocean, Galle Harbour, and the southern coast, blending maritime history with colonial architecture.

        Historical Layers:

         * British Era: The original lighthouse (1848) used a mercury bath to stabilize its rotating prism, exposing keepers to toxic fumes.

         * 1939 Rebuild: The current concrete tower replaced the iron structure destroyed by fire, standing 100 meters from the original site.

         * UNESCO Context: Part of Galle Fort's “fusion of European architecture and South Asian traditions”.
        """,
        Point(80.219352, 6.024555, srid=4326)
    ),
    (
        "Point Utrecht Bastion", 
        Polygon([
            (6.0247, 80.219468),
            (6.024702, 80.219535),
            (6.02438, 80.219612),
            (6.024369, 80.219307),
            (6.024585, 80.219342),
            (6.0247, 80.219468)
        ]), 
        """
        Dutch-Era Defense & Lighthouse Hub
        A 17th-century Dutch bastion built to reinforce Galle Fort's eastern defenses, Point Utrecht Bastion was named after Utrecht, the hometown of the first Dutch clergyman to arrive in Galle in 1641. Though small, it housed six cannons by 1760 and a Dutch inscription from 1782, reflecting its role in compensating for weaknesses in the neighboring rampart. Today, it's best known for hosting the Galle Lighthouse, Sri Lanka's oldest light station, rebuilt by the British in 1939 after a fire destroyed the original 1848 structure.

        Historical Layers:

         * Portuguese Origins: Part of the fort's original defenses, later fortified by the Dutch.

         * Dutch Reinforcement: Strengthened with coral and granite to counter naval threats.

         * UNESCO Context: Part of Galle Fort, a UNESCO World Heritage Site recognized for its fusion of European and South Asian traditions.
        """,
        Point(80.219505, 6.024459, srid=4326)
    ),
    (
        "The Aurora Bastion",
        Polygon([
        (80.219757, 6.026415),
        (80.21991, 6.026329),
        (80.219669, 6.026164),
        (80.219757, 6.026415)
        ]),
        """
        Dutch-Era Defense & Mythical Namesake
        A 17th-century Dutch bastion built to compensate for weaknesses in Galle Fort's northern ramparts, the Aurora Bastion was named after the Roman goddess of the dawn, reflecting its strategic position to monitor early-morning threats. Though small, it housed gun platforms and reinforced the fort's defenses against inland attacks, blending Dutch engineering with mythological flair.

        Historical Context:
         * Dutch Era: Constructed in the 17th century as part of Galle Fort's northern defenses, though too small for major defense.

         * UNESCO Significance: Part of Galle Fort, a UNESCO World Heritage Site recognized for its fusion of European and South Asian traditions.
        """,
        Point(80.219733, 6.026321, srid=4326)
    ),
    (
        "Old BreadFruit Tree",
        Polygon([
        (80.219792, 6.027416),
        (80.219856, 6.027422),
        (80.219859, 6.027379),
        (80.219813, 6.027376),
        (80.219792, 6.027416)

        ]),
        """
        Dutch Legacy & Culinary Icon
        Planted circa 1721 near Akersloot Bastion, this Artocarpus incisisus (breadfruit tree) is Sri Lanka's oldest, introduced by the Dutch as a food source. According to folklore, the Dutch hoped it would sicken locals, but Sri Lankans adapted it into a delicious curry with coconut milk, now a staple dish.

        Historical Context:

         * Dutch Era: Part of colonial efforts to establish sustainable food sources in Galle Fort.

         * UNESCO Significance: Located within Galle Fort, a UNESCO World Heritage Site.

        Cultural Adaptation:

         * Local Cuisine: Breadfruit curry remains a popular dish in Sri Lanka, blending Dutch and Sinhalese traditions.
        """,
        Point(80.219835, 6.027388, srid=4326)
    ),
    (
        "The Akersloot Bastion",
        Polygon([
        (80.219765, 6.027604),
        (80.219867, 6.02765),
        (80.219891, 6.027367),
        (80.219765, 6.027295),
        (80.219765, 6.027604)
        ]),
        """
        Dutch-Era Defense & Harbour Sentinel
        A 17th-century Dutch bastion built to protect Galle Harbour, Akersloot Bastion was named after Akersloot, the Dutch hometown of Admiral Wilhelm Jacobs Coster, who led the Dutch conquest of Galle Fort from the Portuguese in 1640. Strategically positioned behind the Old Dutch Hospital, it housed seven cannons to guard the bay and served as a harbour master's residence under British rule.

        Historical Layers:

         * Portuguese Origins: Part of the fort's original defenses, later fortified by the Dutch.

         * Dutch Reinforcement: Built with coral and granite to counter naval threats, featuring an inscription “Akersloot 1759”.

         * UNESCO Context: Part of Galle Fort, a UNESCO World Heritage Site recognized for its fusion of European and South Asian traditions.

        Views:

         * Overlooks Galle Harbour, Rumassala Hill, and the Dutch Hospital.

        Cultural Legacy:

         * Old Breadfruit Tree: Visible above the bastion, this Artocarpus incisisus is Sri Lanka's oldest, planted by the Dutch circa 1721.
        """,
        Point(80.219787, 6.027479, srid=4326)
    ),
    (
        "The Zwart Bastion",
        Polygon([
        (80.219122, 6.029218),
        (80.219409, 6.029213),
        (80.219441, 6.028909),
        (80.219194, 6.028893),
        (80.219122, 6.029218)
        ]),
        """
        Portuguese Roots & Dutch Legacy
        The Zwart Bastion (Dutch for “Black Fort”) is the only surviving remnant of Galle Fort's original Portuguese defenses, built in 1588 as Santa Cruz to protect the harbor. Later fortified by the Dutch in 1643, it became a holding cell for African slaves and a military prison, earning its name from either smoke-stained walls or its dark history.

        Historical Layers:

         * Portuguese Era: Constructed with palm trees, coral, and mud as a watchtower and Fortaleza.

         * Dutch Reinforcement: Renamed Zwart Bastion in 1643, housing slave cells and later serving as a British-era police headquarters.

         * UNESCO Context: Part of Galle Fort, a UNESCO World Heritage Site recognized for its fusion of European and South Asian traditions.

        Views:

         * Overlooks Galle Harbour and Rumassala Hill, with glimpses of Flag Rock Bastion.
        """,
        Point(80.219317, 6.028874, srid=4326)
    ),
    (
        "The Vismarkt Bastion",
        Polygon([
        (80.217188, 6.0292),
        (80.217335, 6.029221),
        (80.217365, 6.029077),
        (80.217212, 6.029058),
        (80.217188, 6.0292)
        ]),
        """
        Dutch-Era Market Hub & Coastal Defense
        A 17th-century Dutch bastion built to reinforce Galle Fort's eastern defenses, Vismarkt Bastion (Dutch for “Fish Market Bastion”) served as a strategic stronghold to protect the port and local fishing crafts. Though less prominent than other bastions, its coral-and-granite walls reflect Dutch engineering, while its proximity to Galle Harbour underscores its role in safeguarding maritime trade.

        Historical Context:

         * Portuguese Origins: Built in 1588 as part of the original fortifications, later fortified by the Dutch in the 17th century.

         * Dutch Reinforcement: Strengthened with coral and granite to counter naval threats, though smaller than bastions like Sun Bastion.

         * UNESCO Significance: Part of Galle Fort, a UNESCO World Heritage Site recognized for its fusion of European and South Asian traditions.

        Views:

         * Overlooks Galle Harbour and Rumassala Hill, with glimpses of Flag Rock Bastion.
        """,
        Point(80.217255, 6.029092, srid=4326)
    ),
    (
        "Police Residental Building",
        Polygon([
            (80.216806, 6.029806),
            (80.216841, 6.02963),
            (80.216731, 6.029608),
            (80.216698, 6.029784),
            (80.216806, 6.029806)
        ]),
        """
        Colonial-Era Architecture & Adaptive Reuse
        A 19th-century British-era structure within Galle Fort (a UNESCO World Heritage Site), the Police Residential Building was part of the fort's colonial administrative complex. Originally housing police barracks, it later served as residential quarters for officers before being vacated in 2017 as part of UNESCO-led conservation efforts to preserve the fort's “living heritage”.

        Historical Context:

         * British Era: Built during British rule (1796-1948) to support colonial governance, reflecting Galle's role as a southern administrative hub.

         * UNESCO Conservation: Vacated in 2017 to align with UNESCO's mandate to protect the fort's “fusion of European architecture and South Asian traditions”.

        Adaptive Reuse:

         * Post-2017 Plans: Slated for adaptive reuse (e.g., museums, boutique hotels) to enhance tourism while preserving its colonial-era charm.
        """,
        Point(80.216675, 6.029634, srid=4326)
    ),
    (
        "Galle Services club",
        Polygon([
            (80.215531,6.029898),
            (80.215545,6.029682),
            (80.215835,6.029583),
            (80.216076,6.029602),
            (80.216041,6.029954),
            (80.215531,6.029898)
        ]), 
        """
        Colonial Sports Legacy & Heritage Hub
        Established in 1947 as a successor to the Galle Gymkhana Lawn Tennis Club (founded in 1885), the Galle Services Club is a social and sports institution rooted in colonial-era traditions. Located within Galle Fort (a UNESCO World Heritage Site), it reflects the city's British colonial past, blending sportsmanship with heritage.

        Historical Context:

         * British Era: Replaced the Galle Gymkhana Club (1885), which hosted horse racing and tennis tournaments for European and Ceylonese elites.

         * UNESCO Significance: Part of Galle Fort's “fusion of European architecture and South Asian traditions”.

        Sports Facilities:

         * Tennis Courts: Four hardcourts refurbished in 2021, though controversially due to heritage concerns.

         * Legacy: Once hosted horse racing at the Manning racecourse (now a children's playground).
        """,
        Point(80.215777, 6.029618, srid=4326)
    ),
    (
        "HeadQuarters Second Battalion Gamunu Watch",
        Polygon([
        (80.214194, 6.029177),
        (80.214223, 6.028612),
        (80.214867, 6.028543),
        (80.215267, 6.02878),
        (80.215116, 6.029305),
        (80.214194, 6.029177)

        ]),
        """
        Colonial-Era Barracks & Military Heritage
        Located within Galle Fort (a UNESCO World Heritage Site), the Headquarters Second Battalion Gemunu Watch occupies a British-era structure repurposed for military use. Established in 1964 as the 2nd (Volunteer) Battalion of the Gemunu Watch, it traces its roots to the Volunteer Gemunu Regiment formed in 1959 to absorb troops from the disbanded Ruhunu Regiment.

        Historical Context:

         * Origins: Renamed from the Volunteer Gemunu Regiment in 1964, it became part of the Gemunu Watch, a regiment named after King Gemunu, a legendary Sri Lankan ruler.

         * UNESCO Setting: Housed in a colonial-era building within Galle Fort, reflecting the fort's “fusion of European architecture and South Asian traditions”.

        Military Role:

         * Volunteer Unit: Focuses on counter-insurgency operations and border security, historically deployed in Jaffna and Mannar during the 1971 insurgency.

         * Sacrifices: 06 Officers and 27 Other Ranks killed in action, with 01 Officer and 14 Other Ranks disabled.

         Historical Role:

         * 1959 Origins: Formed as the Volunteer Gemunu Regiment under Capt. D.S. Amarasooriya, later renamed 2nd (Vol) Battalion Gemunu Watch in 1964.

         * Operations: Deployed in Jaffna and Mannar during TAFII (Task Force Anti-Illicit Immigration) and 1971 insurgency.
        """,
        Point(80.214841, 6.028932, srid=4326)
    ),
    (
        "Army Park",
        Polygon([
        (80.215213, 6.028668),
        (80.214848, 6.028404),
        (80.214964, 6.028094),
        (80.215401, 6.028505),
        (80.215213, 6.028668)

        ]),
        """
        Colonial-Era Green Space & Military Legacy
        A public park adjacent to Galle Fort (a UNESCO World Heritage Site), Army Park is nestled near Army Camp and reflects the fort's colonial and military history. Though less documented than Galle's bastions, its proximity to Dharmapala Park (a nearby green space) and Galle Fort's ramparts offers a tranquil escape from the fort's bustling streets.

        Historical Context:

         * Colonial Era: Likely part of British-era military infrastructure, though exact origins unclear.

         * UNESCO Setting: Adjacent to Galle Fort, recognized for its “fusion of European architecture and South Asian traditions”.
        """,
        Point(80.215079, 6.028511, srid=4326)
    ),
    (
        "Magistrate Court",
        Polygon([
        (80.216345, 6.027805),
        (80.216104, 6.027733),
        (80.216144, 6.027584),
        (80.216391, 6.02765),
        (80.216345, 6.027805)
     ]),
        """
        Colonial Justice & Living Heritage
        Located in Galle Fort (a UNESCO World Heritage Site), the Magistrate Court traces its roots to British colonial reforms under Governor Frederick North in 1798, who abolished barbaric punishments like public hangings and established a magistrate's court next to the old Dutch courthouse. Today, it operates within Court Square, a hub of colonial-era justice and modern legal proceedings.

        Historical Context:

         * Dutch Era: The original Dutch courthouse (now adjacent) housed Malay soldiers and hosted public punishments like branding and lashing.

         * British Reforms: Replaced by a magistrate's court in 1798, part of a broader shift to Roman-Dutch law still used in Sri Lanka.

         * UNESCO Significance: Part of Galle Fort's “fusion of European architecture and South Asian traditions”.
        """,
        Point(80.216281, 6.027716, srid=4326)
    ),
    (
        "Shri Sudharmalaya Temple",
        Polygon([
            (80.215364, 6.027098),
            (80.215393, 6.026954),
            (80.215221, 6.026951),
            (80.215213, 6.027069),
            (80.215364, 6.027098)
        ]),
        """
        Buddhist Serenity in a Colonial Setting
        Nestled within Galle Fort (a UNESCO World Heritage Site), Shri Sudharmalaya Temple is the only Buddhist temple in this historic precinct, blending Dutch colonial architecture with traditional Buddhist art. Established in 1889, it reflects Galle's multicultural harmony, standing alongside mosques, churches, and Hindu temples.

        Historical Context:

         * Colonial Roots: Built in a repurposed Dutch-era structure, possibly a former church, with arched windows and stone pillars.

         * UNESCO Significance: Part of Galle Fort's “fusion of European architecture and South Asian traditions”.

        Artistic Highlights:

         * Reclining Buddha: A large statue dominates the prayer hall, flanked by Sariputta and Moggallana (Buddha's disciples).

         * Murals & Carvings: Walls depict Buddhist teachings, while Dutch-era features like a belfry hint at its colonial past.
        """,
        Point(80.215278, 6.027028, srid=4326)
    ),
    (
        "Aroosiyathul Qudiriyaa Taikka",
        Polygon([
        (80.217877, 6.025906),
        (80.217893, 6.025847),
        (80.21781, 6.025831),
        (80.217797, 6.025892),
        (80.217877, 6.025906)

        ]),
        """

        """,
        Point(80.21788, 6.025883, srid=4326)
    ),
    (
        "Zaviya Ummul Fuqarah",
        Polygon([
        (80.217378, 6.024452),
        (80.217724, 6.024556),
        (80.217732, 6.024617),
        (80.217367, 6.024508),
        (80.217378, 6.024452)
        ]),
        """
        Muslim Women's Religious Hub
        A religious center for Muslim women established in 1938, Zaviya Ummul Fuqarah (also spelled Zaviyathul Ummul Fukara) serves as a spiritual and educational space in Galle. Located near Thomas Gall International School and Jiffry Thaikka, it reflects the city's multicultural heritage.

        Historical Context:

         * 1938 Origins: Founded to empower Muslim women through Islamic education and community support.

         * 75th Anniversary: Celebrated in 2013 at Hall De Galle, highlighting its enduring role in Galle's Muslim community.

        Cultural Role:

         * Women-Centric: Focuses on prayer, Quranic studies, and social welfare, fostering interfaith harmony in a city with Dutch, Portuguese, and British colonial roots.
        """,
        Point(80.217397, 6.024488, srid=4326)
    ),
    (
        "Meeran Jumma Masjid",
        Polygon([
            (80.218616, 6.024735),
            (80.218833, 6.024653),
            (80.218782, 6.024517),
            (80.218605, 6.024482),
            (80.218567, 6.02461),
            (80.218616, 6.024735)
        ]),
        """
        Colonial-Era Mosque & Cultural Fusion
        The only mosque within Galle Fort (a UNESCO World Heritage Site), Meeran Jumma Masjid blends Victorian, Baroque, and Islamic architectural styles, reflecting Galle's multicultural legacy. Established in 1904 by Ahamed Haji Ismail, it replaced an earlier mosque from the 1750s, though debates persist about its exact origins.

        Historical Context:

         * Dutch Colonial Roots: Built during Dutch rule, when mosques were permitted unlike under Portuguese governance.

         * UNESCO Significance: Part of Galle Fort's “fusion of European architecture and South Asian traditions”.

        Architectural Highlights:

         * Colonial Design: Resembles a church with stained glass windows, symmetrical arches, and ceramic-tiled floors.

         * Islamic Elements: Features a central dome, Arabic inscriptions, and a mihrab (prayer niche).
        """,
        Point(80.218639, 6.024512, srid=4326)
    ),
    (
        "Zaviya Shazuliyyah",
        Polygon([
        (80.218448, 6.024814),
        (80.21847, 6.024715),
        (80.218612, 6.024739),
        (80.218593, 6.024838),
        (80.218448, 6.024814)

        ]),
        """
        Sufi Spiritual Hub & Educational Legacy
        A Sufi spiritual center rooted in the Shazuliya Tariqa (order), Zaviya Shazuliyyah traces its Sri Lankan origins to 1867, when As-Seyyed Ahamed Ibunu Salihul Yamani introduced the order. While its exact location in Galle Fort is unclear, it is linked to Zaviyathul Ummul Fuqara (a women's zaviya established in 1938) and Makkiya Arabic College, which housed early Shazuliya activities.

        Historical Context:

         * 1867 Origins: Founded by As-Seyyed Ahamed Ibunu Salihul Yamani, who brought the Shazuliya Tariqa to Sri Lanka, emphasizing zikr (devotional chanting) and spiritual purification.

         * UNESCO Setting: Part of Galle Fort's “living heritage”, though not a standalone landmark.

        Educational Role:

         * Makkiya Arabic College: Hosted Shazuliya teachings and later became a hub for Islamic scholarship.

         * Zaviyathul Ummul Fuqara: A women's zaviya (1938) inspired by Shazuliya principles, focusing on prayer and Quranic studies.
        """,
        Point(80.218518, 6.024819, srid=4326)
    ),
    (
        "Historical Mansion Museum",
        Polygon([
        (80.219109, 6.026598),
        (80.218854, 6.026587),
        (80.218865, 6.026366),
        (80.219047, 6.026371),
        (80.219045, 6.026408),
        (80.21912, 6.026416),
        (80.219109, 6.026598)
        ]),
        """
        Colonial-Era Antiques & Living Heritage
        Housed in a restored Dutch colonial mansion within Galle Fort (a UNESCO World Heritage Site), the Historical Mansion Museum showcases a privately owned collection of colonial artifacts, antiques, and traditional crafts. Established by Abdul Gaffer, it blends Dutch architecture with Sri Lankan heritage, offering a glimpse into Galle's multicultural past.

        Historical Context:

         * Dutch Origins: Built during Dutch rule (17th-19th century) as residential quarters for Dutch East India Company officials, later restored in 1988.

         * UNESCO Significance: Part of Galle Fort's “fusion of European architecture and South Asian traditions”.

        Exhibits:

         * Colonial Artifacts: Antique furniture, VOC porcelain, typewriters, cameras, and maps reflecting Dutch and British rule .

         * Traditional Crafts: Beeralu lace embroidery and gem-cutting demonstrations, with sapphires and jewelry for sale.

         * Historic Well: A 1763 well in the courtyard, a relic of Dutch-era infrastructure.
        """,
        Point(80.218901, 6.026454, srid=4326)
    ),
    (
        "Dutch Hospital Shopping Precinct",
        Polygon([
            (80.219445, 6.027203),
            (80.219597, 6.027203),
            (80.219592, 6.026325),
            (80.219436, 6.02633),
            (80.219445, 6.027203)

        ]),
        """
        Colonial Architecture & Modern Luxury
        A 17th-century Dutch colonial building repurposed as a shopping and dining hub, the Dutch Hospital Shopping Precinct is a UNESCO-listed landmark within Galle Fort. Originally built as a hospital for Dutch East India Company personnel (1640-1643), it later served as British-era barracks and post-independence administrative offices before its 2014 restoration.

        Historical Layers:

         * Dutch Era: Constructed on the site of the Portuguese mint, its thick coral-stone walls, teak beams, and colonaded verandas reflect Dutch engineering.

         * British Additions: Expanded in the 19th century with glazed windows and granite floors, later housing the Government Agent's office.

         * UNESCO Context: Part of Galle Fort's “fusion of European architecture and South Asian traditions”.

        Modern Amenities:

         * Restaurants & Bars: Ministry of Crabs, Harpos Café, and Spa Ceylon blend Sri Lankan cuisine with colonial ambiance.

         * Boutique Stores: Barefoot (handmade crafts), ODEL (fashion), and Colombo Jewellery Stores offer local textiles and gemstones.
        """,
        Point(80.219481, 6.026745, srid=4326)
    ),
    (
        "Magister Square",
        Polygon([
        (80.218822, 6.02808),
        (80.218812, 6.027253),
        (80.219394, 6.027365),
        (80.219276, 6.028064),
        (80.21919, 6.028136),
        (80.218822, 6.02808)
        ]),
        """
        Colonial-Era Marketplace & Legal Hub
        A historic marketplace within Galle Fort (a UNESCO World Heritage Site), Magister Square is nestled near Court Square, reflecting the fort's colonial administrative legacy. Though less documented than major landmarks, its proximity to Dutch-era bastions and British-era legal institutions underscores its role in Galle's multicultural heritage.

        Historical Context:

         * Colonial Roots: Part of Galle Fort's grid layout, established by the Dutch in 1669 to organize trade and governance.

         * UNESCO Significance: Part of Galle Fort's “fusion of European architecture and South Asian traditions”.
                """,
        Point(80.219264, 6.027676, srid=4326)
    ),
    (
        "District Court Galle",
        Polygon([
            (80.219331, 6.028),
            (80.219567, 6.02805),
            (80.219706, 6.027575),
            (80.219414, 6.027509),
            (80.219331, 6.028)
        ]),
        """
        Colonial Justice & Architectural Legacy
        Located on Hospital Street within Galle Fort (a UNESCO World Heritage Site), the District Court Galle operates in a 1927 British-era building adjacent to the High Court Complex. Its Dutch-inspired architecture reflects Galle's multicultural legal heritage, blending colonial-era design with South Asian traditions.

        Historical Context:

         * British Era: Built in 1927 during British rule, replacing earlier Dutch-era legal institutions like the Magistrate Court established in 1798.

         * Dutch Roots: The old Dutch courthouse (now adjacent) housed Malay soldiers and hosted public punishments like branding and lashing under Dutch rule.

         * UNESCO Significance: Part of Galle Fort's “fusion of European architecture and South Asian traditions”.

        Architectural Highlights:

         * Dutch Influences: Features oval door windows and square-shaped balconies, echoing Dutch colonial design .

         * British Additions: Symmetrical facades and granite floors reflect British administrative preferences.
        """,
        Point(80.219379, 6.027948, srid=4326)
    ),
    (
        "Galle Fort Dutch Entrance",
        Polygon([
        (80.218534, 6.028282),
        (80.218588, 6.028082),
        (80.2184, 6.028045),
        (80.218352, 6.028239),
        (80.218534, 6.028282)
        ]),
        """
        Portuguese Roots & Dutch Reinforcement
        The Dutch Entrance to Galle Fort refers to the Old Gate, the only surviving remnant of the Portuguese fortifications built in 1588. Later fortified by the Dutch in 1669, it features VOC inscriptions and Dutch-era carvings, blending Portuguese origins with Dutch colonial engineering.

        Historical Context:

         * Portuguese Era: Constructed as part of the original northern defenses, reinforced with palm trees, coral, and mud.

         * Dutch Reinforcement: Renamed Old Gate in 1669, it housed a drawbridge and moat, later replaced by the British with a coat-of-arms.

         * UNESCO Significance: Part of Galle Fort's “fusion of European architecture and South Asian traditions”.

        Architectural Highlights:

         * VOC Inscription: 1669 Dutch East India Company emblem (VOC) flanked by lions and a rooster, symbolizing Dutch rule.

         * British Additions: Coat-of-arms of King George III added later, reflecting British colonial influence.
        """,
        Point(80.218435, 6.028257, srid=4326)
    ),
    (
        "Hall De Galle",
        Polygon([
        (80.218029, 6.028468),
        (80.218177, 6.02838),
        (80.218059, 6.028188),
        (80.217911, 6.02827),
        (80.218029, 6.028468)
        ]),
        """
        Cultural Hub & Colonial-Era Venue
        A public venue within Galle Fort (a UNESCO World Heritage Site), Hall De Galle hosts community events, stage dramas, and cultural gatherings, reflecting the fort's multicultural identity. Though less prominent than bastions or museums, its role as a social and artistic space underscores Galle's living heritage.

        Historical Context:

         * Colonial Roots: Likely built during Dutch or British rule as part of Galle Fort's administrative infrastructure, though exact origins unclear.

         * UNESCO Setting: Part of Galle Fort's “fusion of European architecture and South Asian traditions".

        Cultural Role:

         * Stage Dramas: Hosts Sinhala theater performances and local festivals, blending traditional art with colonial-era architecture.

         * Community Events: Serves as a public space for weddings and cultural workshops.
        """,
        Point(80.21807, 6.028367, srid=4326)
    ),
    (
        "Archeology Regional Office",
        Polygon([
        (80.218145, 6.027933),
        (80.218188, 6.027784),
        (80.218486, 6.027856),
        (80.218448, 6.028002),
        (80.218145, 6.027933)
        ]),
        """
        Conservation Hub & Heritage Management
        Located on Queen's Street within Galle Fort (a UNESCO World Heritage Site), the Archaeology Regional Office oversees conservation efforts and site management in Sri Lanka's Southern Province. Part of the Department of Archaeology, it enforces regulations to protect Galle Fort's “fusion of European architecture and South Asian traditions”.

        Historical Context:

         * UNESCO Role: Manages Galle Fort's preservation, including Dutch-era bastions, colonial-era buildings, and archaeological sites.

         * Colonial-Era Architecture: Housed in a Dutch-era structure within Cheena Koratuwa, a mixed-use neighborhood in Galle Fort.
        """,
        Point(80.218309, 6.027919, srid=4326)
    ),
    (
        "Dutch Reformed Church",
        Polygon([
        (80.217239, 6.02845),
        (80.216887, 6.028261),
        (80.217011, 6.027959),
        (80.217244, 6.028042),
        (80.217228, 6.028093),
        (80.217373, 6.028146),
        (80.217239, 6.02845)
        ]),
        """
        Colonial Baroque & Living Heritage
        A Baroque-style church built by the Dutch in 1755 (completed in 1775), the Groote Kerk (Dutch for “Great Church”) is the oldest Protestant church still in use in Sri Lanka. Situated near the entrance of Galle Fort (a UNESCO World Heritage Site), it blends Dutch colonial architecture with British-era additions, reflecting Galle's multicultural legacy.

        Historical Context:

         * Dutch Origins: Built on the site of a Portuguese Capuchin Convent, its foundations were laid in 1682 but completed decades later by Commandeur Casparus de Jong and his wife as a thanksgiving for their daughter's birth.

         * UNESCO Significance: Part of Galle Fort's “fusion of European architecture and South Asian traditions”.

        Architectural Highlights:

         * Baroque Design: Features intricate stone carvings, vaulted ceilings, and a calamander wood pulpit.

         * Gravestones: The floor is paved with Dutch tombstones from the old cemetery, including those of colonial officials and merchants.

         * British Additions: Stained glass windows (1830), communion rails, and a small organ (early 20th century) reflect British modifications.

         * Belfry: A detached bell tower (1701) with a 1709 bell, relocated after a lightning strike.
        """,
        Point(80.217196, 6.028196, srid=4326)
    ),
    (
        "National Museum Fort",
        Polygon([
        (80.216957, 6.028783),
        (80.217107, 6.028818),
        (80.217013, 6.029079),
        (80.216885, 6.029044),
        (80.216957, 6.028783)
        ]),
        """
        Colonial-Era Architecture & Cultural Heritage
        Housed in the oldest remaining Dutch building in Galle Fort (a UNESCO World Heritage Site), the National Museum Fort (Galle National Museum) showcases Sri Lanka's colonial past and traditional craftsmanship. Built in 1656 as a Dutch commissariat store, it later served as a billiards room for the New Oriental Hotel (now Amangalla Hotel) before its 1986 restoration as a museum esult.

        Historical Context:

         * Dutch Origins: Constructed during Dutch rule to supply the Galle Fort garrison, its colonaded design and thick coral-stone walls reflect Dutch engineering.

         * UNESCO Significance: Part of Galle Fort's “fusion of European architecture and South Asian traditions”.

        Exhibits:

         * Cottage Industries: Beeralu lace weaving, turtle-shell jewelry, and traditional wooden masks highlight Southern Sri Lanka's artisanal heritage.

         * Colonial Artifacts: Dutch-era furniture, VOC porcelain, ship equipment, and weapons (e.g., cannons, swords) from the Dutch and British periods.

         * Sri Lanka-China Friendship Gallery: Explores historical trade ties, including Buddhist monk Faxian and Admiral Zheng He's 14th-century voyages.
        """,
        Point(80.217016, 6.028948, srid=4326)
    ),  
]

for name, polygon, description, main_point in sub_geofences_data:
    sub_geofences, created = SubGeofence.objects.get_or_create(
        name = name,
        main_geofence = galle_fort,
        defaults= {
            'location': polygon,
            'description': description,
            'main_point' : main_point
        }
    )
    if created:
        print("New SubGeofence created:", sub_geofences)
    else:
        print("SubGeofence already exists:", sub_geofences)

print("Galle Fort and its SubGeofences have been saved successfully!")


# Create a new Geofence and its SubGeofences
# Geofence: "testing"

test_latlngs = [
    (80.19810835559713, 6.0738677971490755),
    (80.19800612104495, 6.071974969483788),
    (80.19455935614272, 6.071805534457907),          
    (80.19454961951871, 6.07341758554526),
    (80.19810835559713, 6.0738677971490755)
]

test_polygon_obj = Polygon(test_latlngs)

test_geofence, test_geofence_created = MainGeofence.objects.get_or_create(
    name='Test Main Geofence',
    defaults={
        'location': test_polygon_obj,
        'description': """
                        This is a test Geofence for testing purposes.
                        """,
        'main_point' : Point(80.19482712012793, 6.072571206312612, srid=4326)
    }
)
if test_geofence_created:
    print("New MainGeofence created:", test_geofence)
else:
    print("MainGeofence already exists:", test_geofence)

# SubGeofences for the "testing" Geofence

test_sub_geofences_data = [
    (
        "Test SubGeofence 1",
        Polygon([
        ( 80.19716044324244, 6.073218863203539),
        (80.19711283403497, 6.073220863569845),
        (80.1970994229906 ,6.073138848545217),
        (80.19715507882468,6.073114177356497),
        (80.19716044324244, 6.073218863203539)
        ]),
        """
        Sub Geofence 1 Description
        """,
        Point(80.1971496477765, 6.07316985259187, srid=4326)
    ),  
    (
        "Test SubGeofence 2",
        Polygon([
        (80.19787994071079,6.073110188942325),
        (80.19804891986973, 6.073051511515538),
        (80.19800131066225, 6.072924154805867),
        (80.1978470836521, 6.072952159948808),
        (80.19787994071079,6.073110188942325)
        ]),
        """
        Sub Geofence 2 Description
        """,
        Point(80.19793029723023, 6.073000429860537, srid=4326)
    ),  
]

for name, polygon, description, main_point in test_sub_geofences_data:
    test_sub_geofences, test_sub_geofence_created = SubGeofence.objects.get_or_create(
        name = name,
        main_geofence = test_geofence,
        defaults= {
            'location': polygon,
            'description': description,
            'main_point' : main_point
        }
    )
    if test_sub_geofence_created:
        print("New SubGeofence created:", test_sub_geofences)
    else:
        print("SubGeofence already exists:", test_sub_geofences)

print("Test geofence and its SubGeofences have been saved successfully!")