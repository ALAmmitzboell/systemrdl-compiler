from unittest_utils import RDLSourceTestCase

class TestPropRefs(RDLSourceTestCase):

    def test_prop_value_ref(self):
        root = self.compile(
            ["rdl_src/prop_ref.rdl"],
            "prop_value_ref"
        )
        a = root.find_by_path("prop_value_ref.y.a")
        ref = root.find_by_path("prop_value_ref.y.b").get_property('next')
        self.assertRegex(
            str(ref),
            r"<PropRef_reset prop_value_ref.y.a->reset at 0x\w+>"
        )

        self.assertEqual(ref.node, a)
        self.assertEqual(ref.name, "reset")


    def test_inferred_vector(self):
        root = self.compile(
            ["rdl_src/prop_ref.rdl"],
            "inferred_vector"
        )
        a = root.find_by_path("inferred_vector.y.a")
        we_ref = root.find_by_path("inferred_vector.y.b").get_property('next')
        wel_ref = root.find_by_path("inferred_vector.y.c").get_property('next')

        self.assertEqual(we_ref.node, a)
        self.assertEqual(we_ref.name, "we")

        self.assertEqual(wel_ref.node, a)
        self.assertEqual(wel_ref.name, "wel")


    def test_err_missing_reset(self):
        self.assertRDLCompileError(
            ["rdl_src/prop_ref.rdl"],
            "err_missing_reset",
            r"Assignment references the value of property 'reset', but its value was never set for instance 'a'"
        )


    def test_err_circular_ref(self):
        self.assertRDLCompileError(
            ["rdl_src/prop_ref.rdl"],
            "err_circular_ref",
            r"Assignment creates a circular reference"
        )


    def test_err_no_inferred(self):
        self.assertRDLCompileError(
            ["rdl_src/prop_ref.rdl"],
            "err_no_inferred",
            r"Assignment references property 'we', but the signal it represents was never defined or enabled for instance 'a'"
        )


    def test_err_not_a_counter(self):
        self.assertRDLCompileError(
            ["rdl_src/prop_ref.rdl"],
            "err_not_a_counter",
            r"Reference to property 'incr' is illegal because 'a' is not a counter"
        )


    def test_err_no_counter_threshold(self):
        self.assertRDLCompileError(
            ["rdl_src/prop_ref.rdl"],
            "err_no_counter_threshold",
            r"Reference to property 'incrthreshold' is illegal because the target field does not define any thresholds"
        )
