

# GLOBAL CHOICES :
GENERIC_SIZE_CHOICES = (
    ('37', 37),
    ('38', 38),
    ('39', 39),
    ('40', 40),
    ('41', 40),
    ('42', 42),
    ('43', 43),
    ('44', 44),
    ('45', 45),
)

TSHIRT_SIZE_CHOICES = (
    ('S', 'S'),
    ('L', 'L'),
    ('M', 'M'),
    ('XL', 'XL'),
    ('XS', 'XS'),
    ('XXL', 'XXL'),
)

SCREEN_SIZE_CHOICES = (
    (3.5, '3.5"'),
    (4, '4"'),
    (4.5, '4.5"'),
    (4.7, '4.7"'),
    (5, '5"'),
    (5.1, '5.1"'),
    (5.2, '5.2"'),
    (5.5, '5.5"'),
    (5.7, '5.7"'),
    (6, '6'),
    (7, '7"'),
    (8, '8"'),
    (10, '10"'),
)

BRAND_CHOICES = (
    (100, 'Apple'),
    (101, 'Samsung'),
    (102, 'LG'),
    (103, 'Huawai'),
    (104, 'Motorola'),
    (105, 'Microsoft'),
    (106, 'Lumia'),
    (107, 'HTC'),
    (108, 'ZTE'),
    (109, 'ALCATEL'),
    (200, 'ASUS'),
    (201, 'Nokia'),
    (202, 'Nexus'),

)

MEMORY_SIZE_CHOICES = (
    (8, '8GB'),
    (16, '16GB'),
    (32, '32GB'),
    (64, '64GB'),
    (128, '128GB'),
)

RAM_SIZE_CHOICES = (
    (512, '512MB'),
    (1, '1GB'),
    (2, '2GB'),
    (3, '3GB'),
    (4, '4GB'),
    (8, '8GB'),
)

CAMERA_RESOLUTION_CHOICES = (
    (2, '2MP'),
    (5, '5MP'),
    (8, '8MP'),
    (10, '10MP'),
    (13, '13MP'),
    (16, '16MP'),
    (20, '20MP'),
    (21, '21MP'),
)


SIM_CARD_CONF_CHOICES = (
    ('NO SIM', 'NO SIM'),
    ('STANDARD', 'STANDARD'),
    ('DUAL SIM', 'DUAL SIM'),
    ('TRIO SIM', 'TRIO SIM'),
)

PARFUMS_QUANTITY_CHOICES = (
    (1, '1ml'),
    (2, '2ml'),
    (10, '10ml'),
    (20, '20ml'),
    (30, '30ml'),
    (40, '40ml'),
    (50, '50ml'),
    (60, '60ml'),
    (70, '70ml'),
    (80, '80ml'),
    (90, '90ml'),
    (100, '100ml'),
    (110, '110ml'),
    (150, '150ml'),
    (200, '200ml'),
)

GENDER_CHOICES = (
    ('HOMME', 'H'),
    ('FEMME', 'F'),
)

PARFUM_TYP_CHOICES = (
    ('EDP', 'Eau de Parfum'),
    ('EDT', 'Eau de Toilette'),
    ('Cologne', 'Eau de Cologne'),
    ('Set', 'Coffret'),
)

category_codes_context = {
    'mode': 1050,
    'parfumerie': 2000,
    'smartphone': 2055,
}
