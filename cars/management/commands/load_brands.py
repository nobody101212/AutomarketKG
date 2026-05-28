from django.core.management.base import BaseCommand
from cars.models import Brand, CarModel


class Command(BaseCommand):
    help = 'Загрузка марок и моделей автомобилей'

    def handle(self, *args, **options):
        brands_data = {
            'Toyota': ['Camry', 'Corolla', 'Land Cruiser 200', 'Land Cruiser Prado', 'RAV4', 'Highlander', 'Fortuner', 'Hilux', 'Yaris', 'Avensis', 'Mark II', 'Vitz', 'Estima', 'Alphard', 'Harrier', 'Crown', 'Supra', 'C-HR', 'Sequoia', 'Tundra'],
            'BMW': ['3 Series', '5 Series', '7 Series', 'X1', 'X3', 'X5', 'X6', 'X7', 'M3', 'M5', 'i3', 'i8', 'Z4', '1 Series', '2 Series', '4 Series', '6 Series', '8 Series'],
            'Mercedes-Benz': ['C-Class', 'E-Class', 'S-Class', 'A-Class', 'GLA', 'GLC', 'GLE', 'GLS', 'G-Class', 'CLA', 'CLS', 'AMG GT', 'EQC', 'Vito', 'Sprinter'],
            'Audi': ['A3', 'A4', 'A6', 'A8', 'Q3', 'Q5', 'Q7', 'Q8', 'TT', 'R8', 'RS6', 'S4', 'S6', 'A5', 'A7'],
            'Volkswagen': ['Polo', 'Golf', 'Passat', 'Tiguan', 'Touareg', 'Jetta', 'Arteon', 'T-Cross', 'T-Roc', 'Atlas', 'Caddy', 'Amarok'],
            'Hyundai': ['Solaris', 'Elantra', 'Sonata', 'Tucson', 'Santa Fe', 'Creta', 'Accent', 'i30', 'Palisade', 'Kona', 'Genesis', 'Porter'],
            'Kia': ['Rio', 'Cerato', 'Optima', 'Sportage', 'Sorento', 'Soul', 'Picanto', 'Stinger', 'Seltos', 'K5', 'Carnival', 'Mohave'],
            'Lexus': ['ES', 'IS', 'LS', 'RX', 'NX', 'LX', 'GX', 'UX', 'RC', 'LC', 'GS'],
            'Honda': ['Civic', 'Accord', 'CR-V', 'Pilot', 'Fit', 'HR-V', 'Odyssey', 'Stepwgn', 'Freed', 'Vezel'],
            'Nissan': ['Almera', 'Teana', 'X-Trail', 'Qashqai', 'Murano', 'Patrol', 'Pathfinder', 'Juke', 'Note', 'Leaf', 'GT-R', 'Sunny'],
            'Mazda': ['Mazda3', 'Mazda6', 'CX-3', 'CX-5', 'CX-9', 'MX-5', 'CX-30', 'Demio', 'Axela', 'Atenza'],
            'Mitsubishi': ['Lancer', 'Outlander', 'Pajero', 'ASX', 'Eclipse Cross', 'L200', 'Montero', 'Galant', 'Delica'],
            'Subaru': ['Impreza', 'Forester', 'Outback', 'Legacy', 'XV', 'WRX', 'Levorg', 'Tribeca'],
            'Chevrolet': ['Cruze', 'Malibu', 'Captiva', 'Tahoe', 'Cobalt', 'Spark', 'Aveo', 'Lacetti', 'Camaro', 'Tracker', 'Equinox'],
            'Ford': ['Focus', 'Mondeo', 'Fiesta', 'Kuga', 'Explorer', 'Mustang', 'Escape', 'Edge', 'Ranger', 'Transit', 'Fusion'],
            'Land Rover': ['Range Rover', 'Discovery', 'Defender', 'Range Rover Sport', 'Range Rover Velar', 'Range Rover Evoque', 'Freelander'],
            'Porsche': ['Cayenne', 'Macan', 'Panamera', '911', 'Cayman', 'Boxster', 'Taycan'],
            'Volvo': ['XC90', 'XC60', 'XC40', 'S60', 'S90', 'V40', 'V60', 'V90'],
            'Jeep': ['Grand Cherokee', 'Wrangler', 'Cherokee', 'Compass', 'Renegade', 'Patriot'],
            'Infiniti': ['Q50', 'Q70', 'QX50', 'QX60', 'QX70', 'QX80', 'FX35', 'G25'],
            'Suzuki': ['Swift', 'Vitara', 'Grand Vitara', 'Jimny', 'SX4', 'Baleno', 'Escudo'],
            'Daewoo': ['Nexia', 'Matiz', 'Gentra', 'Lanos', 'Damas', 'Lacetti'],
            'Renault': ['Logan', 'Sandero', 'Duster', 'Megane', 'Kaptur', 'Arkana', 'Fluence', 'Koleos'],
            'Skoda': ['Octavia', 'Rapid', 'Superb', 'Kodiaq', 'Fabia', 'Karoq', 'Yeti'],
            'Lada': ['Granta', 'Vesta', 'Niva', 'Largus', 'Priora', 'Kalina', 'XRAY', '2107', '2114'],
            'Chery': ['Tiggo 4', 'Tiggo 7', 'Tiggo 8', 'Arrizo 8', 'Tiggo 2', 'Bonus'],
            'Haval': ['Jolion', 'F7', 'H6', 'Dargo', 'H9', 'F7x'],
            'Geely': ['Coolray', 'Atlas', 'Emgrand', 'Tugella', 'Monjaro', 'Okavango'],
            'BYD': ['Han', 'Tang', 'Song', 'Yuan', 'Seal', 'Atto 3', 'Dolphin'],
            'Changan': ['CS35', 'CS55', 'CS75', 'UNI-T', 'UNI-K', 'Alsvin', 'Eado'],
            'Tesla': ['Model 3', 'Model S', 'Model X', 'Model Y'],
            'Datsun': ['on-DO', 'mi-DO'],
            'UAZ': ['Patriot', 'Hunter', 'Buhanka', '469', 'Pickup'],
            'GAZ': ['Gazelle', 'Volga', 'Sobol', 'Gazelle Next'],
            'Peugeot': ['308', '408', '508', '2008', '3008', '5008', 'Partner'],
            'Citroen': ['C4', 'C5', 'Berlingo', 'C3', 'C-Elysee'],
            'Opel': ['Astra', 'Insignia', 'Mokka', 'Corsa', 'Zafira', 'Vectra'],
            'Fiat': ['500', 'Punto', 'Albea', 'Doblo', 'Tipo'],
            'Acura': ['MDX', 'RDX', 'TLX', 'ZDX', 'TSX'],
            'Cadillac': ['Escalade', 'CTS', 'SRX', 'XT5', 'ATS'],
            'Chrysler': ['300C', 'Pacifica', 'Sebring'],
            'Dodge': ['Charger', 'Challenger', 'Durango', 'Journey'],
            'Jaguar': ['XF', 'XE', 'F-Pace', 'XJ', 'E-Pace'],
            'Mini': ['Cooper', 'Countryman', 'Clubman'],
            'Smart': ['ForTwo', 'ForFour'],
            'SsangYong': ['Actyon', 'Rexton', 'Kyron', 'Tivoli'],
            'Isuzu': ['D-Max', 'MU-X', 'Trooper'],
            'Great Wall': ['Hover', 'Wingle', 'Poer'],
            'FAW': ['Besturn', 'V5', 'X80'],
            'JAC': ['S3', 'S5', 'J7', 'T6'],
            'Zeekr': ['001', '007', 'X'],
            'Exeed': ['TXL', 'VX', 'LX'],
            'Tank': ['300', '500'],
            'Li Auto': ['L7', 'L8', 'L9'],
            'Bentley': ['Continental', 'Bentayga', 'Flying Spur'],
            'Rolls-Royce': ['Phantom', 'Ghost', 'Cullinan'],
            'Ferrari': ['488', 'Roma', 'F8', 'Portofino'],
            'Lamborghini': ['Urus', 'Huracan', 'Aventador'],
            'Maserati': ['Levante', 'Ghibli', 'Quattroporte'],
        }

        created = 0
        for brand_name, models_list in brands_data.items():
            brand, _ = Brand.objects.get_or_create(name=brand_name)
            for model_name in models_list:
                _, c = CarModel.objects.get_or_create(brand=brand, name=model_name)
                if c:
                    created += 1

        self.stdout.write(self.style.SUCCESS(
            f'Готово! Марок: {Brand.objects.count()}, Моделей: {CarModel.objects.count()}'
        ))