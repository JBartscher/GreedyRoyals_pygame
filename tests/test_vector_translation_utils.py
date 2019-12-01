from unittest import TestCase

from numpy.testing import assert_array_equal

from utils.vector_translation_utils import *


class TestTranslateUtil(TestCase):

    def test_calculate_center_point(self):
        """
        test calculate_center_point
        """
        v_expect = np.array([50, 50])
        v_actual = calculate_center_point(100, 100)
        assert_array_equal(v_expect, v_actual)

    def test_transform_coordinate_array_to_homogeneous_translation_matrix(self):
        """
        test transform_coordinate_array_to_homogeneous_translation_matrix
        """
        v = np.array([2, 4])
        v_expect = np.array([[1, 0, 2], [0, 1, 4], [0, 0, 1]])
        v_actual = transform_coordinate_array_to_homogeneous_translation_matrix(v)
        assert_array_equal(v_expect, v_actual)

    def test_transform_homogeneous_coordinates_to_coordinate_array(self):
        """
        test transform_homogeneous_coordinates_to_coordinate_array
        """
        v_h = np.array([[2], [4], [1]])
        v_expect = np.array([2, 4])
        v_actual = transform_homogeneous_coordinates_to_coordinate_array(v_h)
        assert_array_equal(v_expect, v_actual)

    def test_transform_coordinate_array_to_homogeneous_coordinates(self):
        """
        test transform_coordinate_array_to_homogeneous_coordinates
        """
        v = np.array([2, 4])
        v_expect = np.array([[2], [4], [1]])
        v_actual = transform_coordinate_array_to_homogeneous_coordinates(v)
        assert_array_equal(v_expect, v_actual)

    def test_translate_coordinates(self):
        """
        test translate_coordinates
        """
        v1 = np.array([5, 3])
        v2 = np.array([3, 5])

        v_expect = np.array([8, 8])
        v_actual = translate_coordinates(v1, v2)
        assert_array_equal(v_expect, v_actual)

    def test_normal_vector(self):
        """
        test normal_vector
        """
        v1 = np.array([2, 1])
        v2 = np.array([1, 2])
        # Test 1
        v_expect = np.array([1, 1])
        v_actual = normal_vector(v1, v2)
        assert_array_equal(v_expect, v_actual)

        # Test 2
        v_expect = np.array([1, 2])
        v_actual = normal_vector([2, 2], [0, 3])
        assert_array_equal(v_expect, v_actual)

    def test_normalize_vector(self):
        """
        test normalize_vector
        """
        v = np.array([2, 2])
        v_expect = np.array([0.707, 0.707])
        v_actual = normalize_vector(v)
        assert_array_equal(v_expect, v_actual)

    def test_calculate_vector_angle_in_degree(self):
        """
        test if the correct angles are returned for a set of movement vectors.
        """
        self.assertAlmostEqual(calculate_vector_angle_in_degree(np.array([1, 0])), 0)  # 0°
        self.assertAlmostEqual(calculate_vector_angle_in_degree(np.array([1, 1])), 45)  # 45°
        self.assertAlmostEqual(calculate_vector_angle_in_degree(np.array([0, 1])), 90)  # 90°
        self.assertAlmostEqual(calculate_vector_angle_in_degree(np.array([-1, 1])), 135)  # 135°
        self.assertAlmostEqual(calculate_vector_angle_in_degree(np.array([-1, 0])), 180)  # 180°
        self.assertAlmostEqual(calculate_vector_angle_in_degree(np.array([-1, -1])), 225)  # 225°
        self.assertAlmostEqual(calculate_vector_angle_in_degree(np.array([0, -1])), 270)  # 270°
        self.assertAlmostEqual(calculate_vector_angle_in_degree(np.array([1, -1])), 315)  # 315°

        self.assertAlmostEqual(calculate_vector_angle_in_degree(np.array([-3, 1])), 161.57)  # 161.5650

    def test_mirror_at_half_by_x_axis(self):
        """
        test mirror_at_half_by_x_axis
        """
        v = np.array([2, 10])
        v_expect = np.array([2, 350])
        v_actual = mirror_at_half_by_x_axis(v, 360)
        assert_array_equal(v_expect, v_actual)

        v = np.array([2, 350])
        v_expect = np.array([2, 10])
        v_actual = mirror_at_half_by_x_axis(v, 360)
        assert_array_equal(v_expect, v_actual)

    def test_compare_2d_array(self):
        """
        test compare_2d_array
        """
        v = np.array([2.4, 10.999])
        u = np.array([1.9, 11.1])
        self.assertTrue(compare_2d_array(v, u))
        v = np.array([2.6, 10.999])
        u = np.array([1.9, 11.1])
        self.assertFalse(compare_2d_array(v, u))
