from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError
from .models import Destination
from .validators import validate_image_extension, validate_image_size



class DestinationImageModelTests(TestCase):
    """Tests para el campo image del modelo Destination"""
    
    def setUp(self):
        """Configuración inicial para cada test"""
        # Crear una imagen de prueba válida (1x1 pixel PNG)
        self.valid_image = SimpleUploadedFile(
            name='test_image.png',
            content=b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82',
            content_type='image/png'
        )
        
        # Crear una imagen JPG válida (mínima)
        self.valid_jpg = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00\xff\xdb\x00C\x00\x08\x06\x06\x07\x06\x05\x08\x07\x07\x07\t\t\x08\n\x0c\x14\r\x0c\x0b\x0b\x0c\x19\x12\x13\x0f\x14\x1d\x1a\x1f\x1e\x1d\x1a\x1c\x1c $.\' ",#\x1c\x1c(7),01444\x1f\'9=82<.342\xff\xc0\x00\x0b\x08\x00\x01\x00\x01\x01\x01\x11\x00\xff\xc4\x00\x1f\x00\x00\x01\x05\x01\x01\x01\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\xff\xc4\x00\xb5\x10\x00\x02\x01\x03\x03\x02\x04\x03\x05\x05\x04\x04\x00\x00\x01}\x01\x02\x03\x00\x04\x11\x05\x12!1A\x06\x13Qa\x07"q\x142\x81\x91\xa1\x08#B\xb1\xc1\x15R\xd1\xf0$3br\x82\t\n\x16\x17\x18\x19\x1a%&\'()*456789:CDEFGHIJSTUVWXYZcdefghijstuvwxyz\x83\x84\x85\x86\x87\x88\x89\x8a\x92\x93\x94\x95\x96\x97\x98\x99\x9a\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xff\xda\x00\x08\x01\x01\x00\x00?\x00\xfe\xfe\xa2\x8a(\xff\xd9',
            content_type='image/jpeg'
        )
    
    def test_destination_creation_with_image(self):
        """Test: Crear destino con imagen válida"""
        destination = Destination.objects.create(
            name='París',
            description='La ciudad de la luz',
            image=self.valid_image
        )
        
        self.assertIsNotNone(destination.image)
        self.assertTrue(destination.image.name.startswith('destinations/'))
        self.assertEqual(destination.name, 'París')
        
        # Limpiar archivo creado
        if destination.image:
            destination.image.delete()
    
    def test_destination_creation_without_image(self):
        """Test: Crear destino sin imagen (campo opcional)"""
        destination = Destination.objects.create(
            name='Londres',
            description='Capital del Reino Unido'
        )
        
        self.assertFalse(destination.image)
        self.assertEqual(destination.name, 'Londres')
    
    def test_destination_image_jpg_format(self):
        """Test: Crear destino con imagen JPG"""
        destination = Destination.objects.create(
            name='Roma',
            description='La ciudad eterna',
            image=self.valid_jpg
        )
        
        self.assertIsNotNone(destination.image)
        self.assertTrue(destination.image.name.endswith('.jpg'))
        
        # Limpiar archivo creado
        if destination.image:
            destination.image.delete()


class ImageValidatorTests(TestCase):
    """Tests para los validadores de imagen"""
    
    def test_validate_valid_png_extension(self):
        """Test: Validar extensión PNG válida"""
        valid_file = SimpleUploadedFile(
            name='test.png',
            content=b'fake image content',
            content_type='image/png'
        )
        
        # No debe lanzar excepción
        try:
            validate_image_extension(valid_file)
        except ValidationError:
            self.fail("validate_image_extension lanzó ValidationError inesperadamente")
    
    def test_validate_valid_jpg_extension(self):
        """Test: Validar extensión JPG válida"""
        valid_file = SimpleUploadedFile(
            name='test.jpg',
            content=b'fake image content',
            content_type='image/jpeg'
        )
        
        try:
            validate_image_extension(valid_file)
        except ValidationError:
            self.fail("validate_image_extension lanzó ValidationError inesperadamente")
    
    def test_validate_invalid_extension(self):
        """Test: Rechazar extensión inválida (.txt)"""
        invalid_file = SimpleUploadedFile(
            name='test.txt',
            content=b'not an image',
            content_type='text/plain'
        )
        
        with self.assertRaises(ValidationError):
            validate_image_extension(invalid_file)
    
    def test_validate_file_size_within_limit(self):
        """Test: Validar tamaño de archivo dentro del límite"""
        # Crear archivo pequeño (menos de 5MB)
        small_file = SimpleUploadedFile(
            name='small.jpg',
            content=b'x' * (1024 * 1024),  # 1MB
            content_type='image/jpeg'
        )
        
        try:
            validate_image_size(small_file)
        except ValidationError:
            self.fail("validate_image_size lanzó ValidationError inesperadamente")
    
    def test_validate_file_size_exceeds_limit(self):
        """Test: Rechazar archivo que excede el límite de tamaño"""
        # Crear archivo grande (más de 20MB)
        # Nota: SimpleUploadedFile necesita tener el atributo size calculado
        content = b'x' * (21 * 1024 * 1024)  # 21MB
        large_file = SimpleUploadedFile(
            name='large.jpg',
            content=content,
            content_type='image/jpeg'
        )
        
        # Asegurarse de que el tamaño esté establecido
        large_file.size = len(content)
        
        with self.assertRaises(ValidationError):
            validate_image_size(large_file)


class DestinationImageUITests(TestCase):
    """Tests de integración para visualización de imágenes en UI"""
    
    def setUp(self):
        """Configuración inicial: crear destinos con y sin imagen"""
        # Crear imagen de prueba válida
        self.test_image = SimpleUploadedFile(
            name='test_paris.png',
            content=b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82',
            content_type='image/png'
        )
        
        # Destino con imagen
        self.destination_with_image = Destination.objects.create(
            name='París',
            description='La ciudad de la luz',
            image=self.test_image
        )
        
        # Destino sin imagen
        self.destination_without_image = Destination.objects.create(
            name='Londres',
            description='Capital del Reino Unido'
        )
    
    def tearDown(self):
        """Limpiar archivos de imagen después de cada test"""
        if self.destination_with_image.image:
            self.destination_with_image.image.delete()
    
    def test_destination_list_shows_image_for_destination_with_image(self):
        """Test: Lista muestra imagen real para destinos con imagen"""
        response = self.client.get('/destinations/')
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.destination_with_image.image.url)
        self.assertContains(response, f'alt="Imagen de {self.destination_with_image.name}"')
    
    def test_destination_list_shows_placeholder_for_destination_without_image(self):
        """Test: Lista muestra placeholder para destinos sin imagen"""
        response = self.client.get('/destinations/')
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'placeholder-destination.svg')
        self.assertContains(response, f'alt="Imagen placeholder para {self.destination_without_image.name}"')
    
    def test_destination_detail_shows_image_with_correct_classes(self):
        """Test: Detalle muestra imagen con clases CSS correctas"""
        response = self.client.get(f'/destination/{self.destination_with_image.id}')
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'destination-detail-image')
        self.assertContains(response, self.destination_with_image.image.url)
        self.assertContains(response, f'alt="Imagen de {self.destination_with_image.name}"')
    
    def test_destination_detail_shows_placeholder_with_correct_classes(self):
        """Test: Detalle muestra placeholder con clases CSS correctas"""
        response = self.client.get(f'/destination/{self.destination_without_image.id}')
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'destination-detail-image')
        self.assertContains(response, 'destination-placeholder')
        self.assertContains(response, 'placeholder-destination.svg')
    
    def test_destination_list_thumbnail_has_correct_structure(self):
        """Test: Thumbnails en lista tienen estructura HTML correcta"""
        response = self.client.get('/destinations/')
        
        self.assertEqual(response.status_code, 200)
        # Verificar que existe el wrapper
        self.assertContains(response, 'destination-thumbnail-wrapper')
        # Verificar que existe la clase thumbnail
        self.assertContains(response, 'destination-thumbnail')
        # Verificar que existe la clase de item
        self.assertContains(response, 'destination-item')
    
    def test_all_destination_images_have_alt_text(self):
        """Test: Todas las imágenes de destinos tienen atributo alt (accesibilidad)"""
        # Test en lista: verificar que las imágenes de destinos tienen alt
        response_list = self.client.get('/destinations/')
        self.assertEqual(response_list.status_code, 200)
        
        # Verificar que las imágenes de destino tienen alt específico
        self.assertContains(response_list, f'alt="Imagen de {self.destination_with_image.name}"')
        self.assertContains(response_list, f'alt="Imagen placeholder para {self.destination_without_image.name}"')
        
        # Test en detalle
        response_detail = self.client.get(f'/destination/{self.destination_with_image.id}')
        self.assertEqual(response_detail.status_code, 200)
        self.assertContains(response_detail, f'alt="Imagen de {self.destination_with_image.name}"')
    
    def test_destination_list_wrapper_maintains_dimensions(self):
        """Test: Wrapper de thumbnail mantiene dimensiones consistentes"""
        response = self.client.get('/destinations/')
        
        self.assertEqual(response.status_code, 200)
        # El wrapper debe estar presente para mantener dimensiones
        self.assertContains(response, 'destination-thumbnail-wrapper')
        
    def test_placeholder_svg_is_accessible(self):
        """Test: SVG placeholder es accesible vía static files"""
        from django.conf import settings
        import os
        
        placeholder_path = os.path.join(
            settings.BASE_DIR,
            'relecloud',
            'static',
            'res',
            'img',
            'placeholder-destination.svg'
        )
        
        # Verificar que el archivo existe
        self.assertTrue(os.path.exists(placeholder_path))
