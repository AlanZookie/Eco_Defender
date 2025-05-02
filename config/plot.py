# Narrative sequences with lines and branching choices
PLOT_SEQUENCES = {
    'intro': {
        'lines': [
            "Welcome to EcoCity! This rapidly growing city is facing serious challenges, including rising pollution and increasing deforestation. Your role is crucial—you must guide EcoCity through these environmental crises.",
            "Keep an eye on the indicators at the top-right corner of your screen—they show the city's current pollution and deforestation levels. Always monitor them carefully as you make your decisions.",
            "Now, let's begin your journey towards a greener, healthier EcoCity!"
        ],
        'choices': [
            {'text': "Begin the journey", 'next_seq': 'event_1', 'id': 'begin_journey'}
        ]
    },
    'good_ending': {
        'lines': [
            "Sunlight pours over a transformed EcoCity. The sky is clear, the air crisp, and birds return to nest atop rooftops now covered in green. Around the city's edge, fields once threatened by development now gleam with rows of solar panels.",
            "Wind turbines turn steadily beyond the hills, powering homes without a hint of smoke. Recycling stations hum quietly at street corners as citizens sort their waste with pride. Children laugh in parks where trees grow tall, and rivers sparkle once more.",
            "Your leadership has sparked a movement—a city once on the brink now shines as a global model of sustainability.",
            "You didn't just save EcoCity. You built its future."
        ],
        'choices': [
            {'text': "Quit Game", 'action': 'quit'},
            {'text': "Return to Main Menu", 'action': 'menu'}
        ]
    },
    'bad_ending': {
        'lines': [
            "A suffocating silence settles over EcoCity. The skies remain a permanent shade of gray, and the last tree fell days ago—without anyone noticing. Rivers have turned black, lifeless and still. Birds no longer sing, and even the insects have disappeared.",
            "Hospitals are overflowing, but medicine cannot cure poisoned air or vanished ecosystems. Children grow up never knowing blue skies or green fields.",
            "What was once a hopeful city has become a cautionary tale—a victim of unchecked growth and neglected responsibility.",
            "The people leave, the buildings decay, and nature turns its back.",
            "You have failed to protect EcoCity."
        ],
        'choices': [
            {'text': "Quit Game", 'action': 'quit'},
            {'text': "Return to Main Menu", 'action': 'menu'}
        ]
    },
    'end_game': {
        'lines': [
            "Congratulations! You have completed all environmental challenges in EcoCity.",
            "Your decisions have shaped the future of our city. The journey towards sustainability continues, but you've made significant progress.",
            "Thank you for being an Eco Defender!"
        ],
        'choices': []
    },
    'event_1': {
        'lines': [
            "Today, you face rising pollution from increasing industrial activities. The air feels heavy, and a gray haze settles over neighborhoods, making it hard to breathe. Hospital visits for respiratory issues have doubled, and children can't play outside without coughing. Local news reports call it an environmental emergency.",
            "What will you do?"
        ],
        'choices': [
            {'text': "Use renewable energy", 'next_seq': 'random_event', 'id': 'pollution_0'},
            {'text': "Set mild rules", 'next_seq': 'random_event', 'id': 'pollution_1'},
            {'text': "Do nothing", 'next_seq': 'random_event', 'id': 'pollution_2'}
        ]
    },
    'event_2': {
        'lines': [
            "Once lush forests now look like patchworks of bare earth. Logging trucks roll in day and night, carrying away what's left of centuries-old trees. The sounds of chirping birds have faded, replaced by the mechanical hum of chainsaws. Some native animals are vanishing completely.",
            "What will you do about deforestation?"
        ],
        'choices': [
            {'text': "Replant trees", 'next_seq': 'random_event', 'id': 'deforestation_0'},
            {'text': "Allow limited logging", 'next_seq': 'random_event', 'id': 'deforestation_1'},
            {'text': "Cut freely", 'next_seq': 'random_event', 'id': 'deforestation_2'}
        ]
    },
    'event_3': {
        'lines': [
            "Trash bins overflow onto sidewalks. Rats scurry through alleyways, and once-beautiful parks are marred by scattered plastic and rotting waste. Tourists avoid the city center, and even residents start wearing masks—not for air, but the stench.",
            "What will you do about waste?"
        ],
        'choices': [
            {'text': "Promote recycling", 'next_seq': 'random_event', 'id': 'pollution_0'},
            {'text': "Small reforms", 'next_seq': 'random_event', 'id': 'pollution_1'},
            {'text': "Dump more", 'next_seq': 'random_event', 'id': 'pollution_2'}
        ]
    },
    'event_4': {
        'lines': [
            "The city's reservoirs are shrinking fast. Some neighborhoods report taps running dry for hours each day. Farmers complain they can't irrigate their fields, and fish in local streams float belly-up as water levels plummet. Anxiety grows as the summer heat shows no mercy.",
            "What's your move?"
        ],
        'choices': [
            {'text': "Enforce water laws", 'next_seq': 'random_event', 'id': 'pollution_0'},
            {'text': "Raise awareness", 'next_seq': 'random_event', 'id': 'pollution_1'},
            {'text': "Ignore it", 'next_seq': 'random_event', 'id': 'pollution_2'}
        ]
    },
    'event_5': {
        'lines': [
            "The streets of EcoCity are louder than ever. Car horns blare, sirens echo, and even late at night, construction noise breaks the silence. People suffer from insomnia. Migratory birds have abandoned their nesting sites. Schools report lower test scores due to constant auditory stress.",
            "What's your solution?"
        ],
        'choices': [
            {'text': "Build sound barriers", 'next_seq': 'random_event', 'id': 'pollution_0'},
            {'text': "Limit car zones", 'next_seq': 'random_event', 'id': 'pollution_1'},
            {'text': "Let it be", 'next_seq': 'random_event', 'id': 'pollution_2'}
        ]
    },
    'event_6': {
        'lines': [
            "Fertilizer run-off from surrounding farms is turning nearby lakes green with algae. Fish die in huge numbers, and fishermen return empty-handed. Children playing in the water develop rashes. The ecosystem is collapsing, and the local economy follows close behind.",
            "How will you respond?"
        ],
        'choices': [
            {'text': "Ban toxic chemicals", 'next_seq': 'random_event', 'id': 'pollution_0'},
            {'text': "Encourage moderation", 'next_seq': 'random_event', 'id': 'pollution_1'},
            {'text': "Allow farming freedom", 'next_seq': 'random_event', 'id': 'pollution_2'}
        ]
    },
    'event_7': {
        'lines': [
            "Heatwaves strike the city harder each year. Without trees or green rooftops, concrete buildings trap heat like ovens. Power usage for air conditioning surges. Elderly citizens suffer the most, with hospitals filling up during every spike in temperature.",
            "Your action?"
        ],
        'choices': [
            {'text': "Green rooftops", 'next_seq': 'random_event', 'id': 'pollution_0'},
            {'text': "Shade zones", 'next_seq': 'random_event', 'id': 'pollution_1'},
            {'text': "Wait it out", 'next_seq': 'random_event', 'id': 'pollution_2'}
        ]
    },
    'event_8': {
        'lines': [
            "Roads are clogged from dawn till dusk. Exhaust fumes hang thick, and commute times double. Pedestrians fear crossing busy intersections, and cyclists have nowhere safe to ride. Public frustration grows louder by the day.",
            "How will you act?"
        ],
        'choices': [
            {'text': "Add bike lanes", 'next_seq': 'random_event', 'id': 'pollution_0'},
            {'text': "Build metro", 'next_seq': 'random_event', 'id': 'pollution_1'},
            {'text': "Widen roads", 'next_seq': 'random_event', 'id': 'pollution_2'}
        ]
    },
    'event_9': {
        'lines': [
            "Waves bring more than sea foam—plastic bags, broken bottles, and bottle caps wash onto the beach. Children playing by the shore step on sharp debris. Marine biologists report turtles with plastic in their stomachs. Tourists turn away in disgust.",
            "Your decision?"
        ],
        'choices': [
            {'text': "Ban plastics", 'next_seq': 'random_event', 'id': 'pollution_0'},
            {'text': "Add bins", 'next_seq': 'random_event', 'id': 'pollution_1'},
            {'text': "Ignore trash", 'next_seq': 'random_event', 'id': 'pollution_2'}
        ]
    },
    'event_10': {
        'lines': [
            "Blackouts sweep across the city during peak hours. Power stations strain to keep up, emitting even more smoke into the sky. Businesses lose productivity, and residents fear that the next outage could last days. EcoCity's future energy stability hangs in the balance.",
            "Next step?"
        ],
        'choices': [
            {'text': "Solar farms", 'next_seq': 'random_event', 'id': 'pollution_0'},
            {'text': "Hybrid mix", 'next_seq': 'random_event', 'id': 'pollution_1'},
            {'text': "Burn more coal", 'next_seq': 'random_event', 'id': 'pollution_2'}
        ]
    },
    'event_11': {
        'lines': [
            "Construction companies are dumping cement waste into the river, changing its pH and threatening aquatic life. Fish are washing up dead near city bridges, and residents complain of a foul chemical smell when walking near the water. Experts warn that if left unchecked, this could permanently disrupt the river's delicate ecosystem and poison groundwater supplies used for drinking.",
            "What will you do about construction pollution?"
        ],
        'choices': [
            {'text': "Fine polluters heavily", 'next_seq': 'random_event', 'id': 'pollution_0'},
            {'text': "Recommend safer disposal", 'next_seq': 'random_event', 'id': 'pollution_1'},
            {'text': "Ignore it", 'next_seq': 'random_event', 'id': 'pollution_2'}
        ]
    },
    'event_12': {
        'lines': [
            "The last patch of old-growth forest near EcoCity is being auctioned to developers. Conservationists are protesting. The towering trees have stood for centuries, sheltering rare birds and filtering the air for nearby neighborhoods. Replacing them with concrete risks flooding, species extinction, and irreversible loss of local biodiversity.",
            "How do you respond to this forest sale?"
        ],
        'choices': [
            {'text': "Protect the forest", 'next_seq': 'random_event', 'id': 'deforestation_0'},
            {'text': "Allow partial use", 'next_seq': 'random_event', 'id': 'deforestation_1'},
            {'text': "Sell it off", 'next_seq': 'random_event', 'id': 'deforestation_2'}
        ]
    },
    'event_13': {
        'lines': [
            "A fireworks festival has worsened the air quality overnight. Schools remain closed due to high particle levels. Emergency rooms report a spike in asthma attacks, and pets across the city show signs of distress. Local scientists say one night's celebration has undone weeks of clean air initiatives.",
            "What's your policy on air events?"
        ],
        'choices': [
            {'text': "Restrict fireworks", 'next_seq': 'random_event', 'id': 'pollution_0'},
            {'text': "Limit duration", 'next_seq': 'random_event', 'id': 'pollution_1'},
            {'text': "Allow them freely", 'next_seq': 'random_event', 'id': 'pollution_2'}
        ]
    },
    'event_14': {
        'lines': [
            "Farms near the border are cutting down buffer trees to make space for more crops, increasing wind erosion. Dust storms now sweep through villages, damaging homes and causing respiratory illness. The loss of these tree lines is making the land more fragile and exposed to climate extremes.",
            "How do you manage farmland?"
        ],
        'choices': [
            {'text': "Restore buffer trees", 'next_seq': 'random_event', 'id': 'deforestation_0'},
            {'text': "Allow regulated clearing", 'next_seq': 'random_event', 'id': 'deforestation_1'},
            {'text': "Do nothing", 'next_seq': 'random_event', 'id': 'deforestation_2'}
        ]
    },
    'event_15': {
        'lines': [
            "A major tech company offers to build new offices in EcoCity—but only if you loosen environmental regulations. While this promises jobs and investment, the blueprints show emissions-heavy operations, limited green space, and aggressive water usage. The city faces a moral crossroads: prosperity now, or sustainability later?",
            "What's your decision?"
        ],
        'choices': [
            {'text': "Reject the deal", 'next_seq': 'random_event', 'id': 'pollution_0'},
            {'text': "Compromise on terms", 'next_seq': 'random_event', 'id': 'pollution_1'},
            {'text': "Accept fully", 'next_seq': 'random_event', 'id': 'pollution_2'}
        ]
    },
    'event_16': {
        'lines': [
            "A series of landslides has blocked city roads. Experts blame unstable, deforested hillsides. Whole communities have been cut off, and cleanup crews risk their lives navigating unstable ground. Locals plead for long-term protection instead of temporary repairs.",
            "What's your response?"
        ],
        'choices': [
            {'text': "Reforest hills", 'next_seq': 'random_event', 'id': 'deforestation_0'},
            {'text': "Add warning signs", 'next_seq': 'random_event', 'id': 'deforestation_1'},
            {'text': "Do nothing", 'next_seq': 'random_event', 'id': 'deforestation_2'}
        ]
    },
    'event_17': {
        'lines': [
            "Recycling facilities are underfunded. Most collected recyclables are being sent to landfills instead. Mountains of plastic and metal waste now pile up on city outskirts, where stray animals and scavengers roam. Citizens begin to lose faith in the city's environmental promises.",
            "How will you handle this?"
        ],
        'choices': [
            {'text': "Boost recycling funds", 'next_seq': 'random_event', 'id': 'pollution_0'},
            {'text': "Encourage citizens", 'next_seq': 'random_event', 'id': 'pollution_1'},
            {'text': "Ignore recycling", 'next_seq': 'random_event', 'id': 'pollution_2'}
        ]
    },
    'event_18': {
        'lines': [
            "A new airport plan threatens a large coastal mangrove forest. The project promises better trade and tourism, but bulldozers are already on standby. The mangroves are the last defense against storm surges and habitat loss for dozens of marine species. Environmental groups warn that without intervention, this coastal buffer will vanish within months.",
            "How do you proceed?"
        ],
        'choices': [
            {'text': "Relocate airport", 'next_seq': 'random_event', 'id': 'deforestation_0'},
            {'text': "Reduce project scale", 'next_seq': 'random_event', 'id': 'deforestation_1'},
            {'text': "Approve fully", 'next_seq': 'random_event', 'id': 'deforestation_2'}
        ]
    },
    'event_19': {
        'lines': [
            "A rising number of diesel generators are used during blackouts, worsening air quality. The constant humming and smell of burning fuel now define city nights. Residents feel trapped indoors, unable to open windows or breathe freely. Doctors report an increase in headaches and respiratory problems.",
            "What's your solution?"
        ],
        'choices': [
            {'text': "Support green backup power", 'next_seq': 'random_event', 'id': 'pollution_0'},
            {'text': "Limit generator hours", 'next_seq': 'random_event', 'id': 'pollution_1'},
            {'text': "Allow freely", 'next_seq': 'random_event', 'id': 'pollution_2'}
        ]
    },
    'event_20': {
        'lines': [
            "Illegal tree cutting is reported in protected forest zones. Satellite data shows clearings expanding weekly. Rangers are outnumbered, and smugglers operate with impunity. Wildlife corridors are being severed, pushing species into dangerous, unfamiliar areas.",
            "Your action?"
        ],
        'choices': [
            {'text': "Deploy rangers", 'next_seq': 'random_event', 'id': 'deforestation_0'},
            {'text': "Increase fines", 'next_seq': 'random_event', 'id': 'deforestation_1'},
            {'text': "Ignore it", 'next_seq': 'random_event', 'id': 'deforestation_2'}
        ]
    },
    'event_21': {
        'lines': [
            "Street vendors are burning plastic as fuel, releasing toxic fumes downtown. Pedestrians cover their faces, and shopkeepers complain of constant headaches. The air smells of melted chemicals, and soot lines the windows of nearby buildings.",
            "How will you handle it?"
        ],
        'choices': [
            {'text': "Ban toxic burning", 'next_seq': 'random_event', 'id': 'pollution_0'},
            {'text': "Promote safer fuels", 'next_seq': 'random_event', 'id': 'pollution_1'},
            {'text': "Let it continue", 'next_seq': 'random_event', 'id': 'pollution_2'}
        ]
    },
    'event_22': {
        'lines': [
            "The zoo's rare plants are dying due to poor air and water conditions. Botanists are helpless as exotic flowers wilt. The decline threatens conservation projects and deters educational visits. Young students ask, 'Why can't we protect even the plants?'",
            "How do you respond?"
        ],
        'choices': [
            {'text': "Improve conditions", 'next_seq': 'random_event', 'id': 'pollution_0'},
            {'text': "Relocate some species", 'next_seq': 'random_event', 'id': 'pollution_1'},
            {'text': "Do nothing", 'next_seq': 'random_event', 'id': 'pollution_2'}
        ]
    },
    'event_23': {
        'lines': [
            "A hillside is being cleared for luxury homes, threatening erosion and species loss. Locals fear flooding during storms, and trails once loved by hikers are now fenced off. Environmentalists call it 'eco-displacement in disguise.'",
            "What will you do?"
        ],
        'choices': [
            {'text': "Halt development", 'next_seq': 'random_event', 'id': 'deforestation_0'},
            {'text': "Reduce footprint", 'next_seq': 'random_event', 'id': 'deforestation_1'},
            {'text': "Approve project", 'next_seq': 'random_event', 'id': 'deforestation_2'}
        ]
    },
    'event_24': {
        'lines': [
            "Old buses idle at terminals for hours, releasing exhaust into busy neighborhoods. Seniors and children living nearby report chronic coughing. The area is visibly covered in black dust. Transit officials say replacements are 'too expensive for now.'",
            "How do you act?"
        ],
        'choices': [
            {'text': "Electrify bus fleets", 'next_seq': 'random_event', 'id': 'pollution_0'},
            {'text': "Enforce no-idle policy", 'next_seq': 'random_event', 'id': 'pollution_1'},
            {'text': "Ignore it", 'next_seq': 'random_event', 'id': 'pollution_2'}
        ]
    },
    'event_25': {
        'lines': [
            "The main river's fish population drops rapidly. Locals suspect chemical dumping. Fishing communities are losing income, and water samples show dangerous contamination. Once a symbol of life, the river now carries illness.",
            "Next move?"
        ],
        'choices': [
            {'text': "Investigate polluters", 'next_seq': 'random_event', 'id': 'pollution_0'},
            {'text': "Test river monthly", 'next_seq': 'random_event', 'id': 'pollution_1'},
            {'text': "Let it be", 'next_seq': 'random_event', 'id': 'pollution_2'}
        ]
    },
    'event_26': {
        'lines': [
            "Grasslands are being paved over for parking lots. Without vegetation, surface temperatures spike, and soil turns infertile. Animals that once grazed here now wander into traffic. Farmers worry about long-term loss of fertile land.",
            "Your policy?"
        ],
        'choices': [
            {'text': "Preserve green zones", 'next_seq': 'random_event', 'id': 'deforestation_0'},
            {'text': "Add green roofs", 'next_seq': 'random_event', 'id': 'deforestation_1'},
            {'text': "Ignore it", 'next_seq': 'random_event', 'id': 'deforestation_2'}
        ]
    },
    'event_27': {
        'lines': [
            "Plastic microbeads from cosmetics are now in drinking water. They've entered the food chain, showing up in shellfish and tap water. Environmental scientists warn that long-term health risks are unknown but concerning.",
            "How do you respond?"
        ],
        'choices': [
            {'text': "Ban microplastics", 'next_seq': 'random_event', 'id': 'pollution_0'},
            {'text': "Encourage filters", 'next_seq': 'random_event', 'id': 'pollution_1'},
            {'text': "No action", 'next_seq': 'random_event', 'id': 'pollution_2'}
        ]
    },
    'event_28': {
        'lines': [
            "Traditional herbal gardens used by locals are being flattened for malls. The community loses access to medicinal plants and cultural rituals. Elders say the land is not just soil—it's memory and survival.",
            "Your plan?"
        ],
        'choices': [
            {'text': "Protect cultural zones", 'next_seq': 'random_event', 'id': 'deforestation_0'},
            {'text': "Replant elsewhere", 'next_seq': 'random_event', 'id': 'deforestation_1'},
            {'text': "Prioritize economy", 'next_seq': 'random_event', 'id': 'deforestation_2'}
        ]
    },
    'event_29': {
        'lines': [
            "Food trucks leak oil and waste into storm drains. These pollutants reach rivers and beaches, causing fish kills. Tourists are warned to avoid waterfront areas. Vendors say they lack proper disposal systems.",
            "How do you solve this?"
        ],
        'choices': [
            {'text': "Enforce eco-rules", 'next_seq': 'random_event', 'id': 'pollution_0'},
            {'text': "Provide training", 'next_seq': 'random_event', 'id': 'pollution_1'},
            {'text': "Do nothing", 'next_seq': 'random_event', 'id': 'pollution_2'}
        ]
    },
    'event_30': {
        'lines': [
            "Riverbanks once home to otters are now crowded with warehouses. Concrete barriers have replaced wetlands. Wildlife cameras show confused animals returning and finding no shelter.",
            "Action?"
        ],
        'choices': [
            {'text': "Restore habitat", 'next_seq': 'random_event', 'id': 'deforestation_0'},
            {'text': "Move some warehouses", 'next_seq': 'random_event', 'id': 'deforestation_1'},
            {'text': "Leave it", 'next_seq': 'random_event', 'id': 'deforestation_2'}
        ]
    }
}
