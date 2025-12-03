from django.test import TestCase
from django.contrib.auth.models import User
from relecloud.models import Review, Destination, Cruise
from django.core.exceptions import ValidationError


class ReviewModelTests(TestCase):
    """Tests para el modelo Review"""

    def setUp(self):
        """Configurar datos de prueba"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.destination = Destination.objects.create(
            name='Marte',
            description='El planeta rojo'
        )
        self.cruise = Cruise.objects.create(
            name='Viaje a Marte',
            description='Crucero a Marte'
        )

    def test_create_review_for_destination(self):
        """Test: crear una reseña para un destino"""
        review = Review.objects.create(
            user=self.user,
            destination=self.destination,
            rating=5,
            title='Increíble experiencia',
            comment='Fue maravilloso visitar Marte'
        )
        self.assertEqual(review.user, self.user)
        self.assertEqual(review.destination, self.destination)
        self.assertEqual(review.rating, 5)
        self.assertTrue(review.id)

    def test_create_review_for_cruise(self):
        """Test: crear una reseña para un crucero"""
        review = Review.objects.create(
            user=self.user,
            cruise=self.cruise,
            rating=4,
            title='Buen viaje',
            comment='Excelente servicio a bordo'
        )
        self.assertEqual(review.cruise, self.cruise)
        self.assertEqual(review.rating, 4)

    def test_review_rating_validation(self):
        """Test: validar que la puntuación está entre 1 y 5"""
        # Puntuación inválida (menor que 1)
        review = Review(
            user=self.user,
            destination=self.destination,
            rating=0,
            title='Mala reseña',
            comment='No me gustó'
        )
        with self.assertRaises(ValidationError):
            review.full_clean()

        # Puntuación inválida (mayor que 5)
        review.rating = 6
        with self.assertRaises(ValidationError):
            review.full_clean()

    def test_unique_review_per_user_destination(self):
        """Test: un usuario solo puede hacer una reseña por destino"""
        Review.objects.create(
            user=self.user,
            destination=self.destination,
            rating=5,
            title='Primera reseña',
            comment='Muy bueno'
        )

        # Intentar crear otra reseña del mismo usuario para el mismo destino
        with self.assertRaises(Exception):
            Review.objects.create(
                user=self.user,
                destination=self.destination,
                rating=3,
                title='Segunda reseña',
                comment='Cambié de opinión'
            )

    def test_review_str_representation(self):
        """Test: verificar la representación en string de Review"""
        review = Review.objects.create(
            user=self.user,
            destination=self.destination,
            rating=5,
            title='Buena reseña',
            comment='Muy interesante'
        )
        self.assertIn(self.user.username, str(review))
        self.assertIn(self.destination.name, str(review))

    def test_review_timestamps(self):
        """Test: verificar que created_at y updated_at se registran correctamente"""
        review = Review.objects.create(
            user=self.user,
            destination=self.destination,
            rating=5,
            title='Test timestamps',
            comment='Prueba de fechas'
        )
        self.assertIsNotNone(review.created_at)
        self.assertIsNotNone(review.updated_at)
        # Los timestamps deben ser muy similares (creados al mismo tiempo)
        time_diff = (review.updated_at - review.created_at).total_seconds()
        self.assertLess(time_diff, 1)  # Menos de 1 segundo de diferencia

    def test_destination_related_reviews(self):
        """Test: verificar que se pueden acceder a las reseñas desde un destino"""
        review = Review.objects.create(
            user=self.user,
            destination=self.destination,
            rating=5,
            title='Reseña destino',
            comment='Excelente'
        )
        self.assertIn(review, self.destination.reviews.all())

    def test_cruise_related_reviews(self):
        """Test: verificar que se pueden acceder a las reseñas desde un crucero"""
        review = Review.objects.create(
            user=self.user,
            cruise=self.cruise,
            rating=4,
            title='Reseña crucero',
            comment='Buen viaje'
        )
        self.assertIn(review, self.cruise.reviews.all())
