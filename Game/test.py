import unittest
import main


class UnitTest(unittest.TestCase):
    def test_unit_constructor(self):
        self.assertTrue(isinstance(main.Swordsman(1, 1), main.Swordsman))
        self.assertTrue(isinstance(main.Archer(1, 1), main.Archer))
        self.assertTrue(isinstance(main.Horseman(1, 1), main.Horseman))
        self.assertTrue(isinstance(main.Lumberjack(1, 1), main.Lumberjack))
        self.assertTrue(isinstance(main.Miner(1, 1), main.Miner))
        self.assertTrue(isinstance(main.Hunter(1, 1), main.Hunter))

    def test_unit_production(self):
        b = main.Barrack(1, 1)
        l = main.LumberjackHut(1, 1)
        m = main.MinerHut(1, 1)
        h = main.HuntersHut(1, 1)
        for i in range(0, 20):
            h.make_unit(h.unit_type[0])
            l.make_unit(l.unit_type[0])
            m.make_unit(m.unit_type[0])
            for j in range(0, 3):
                b.make_unit(b.unit_type[j])

        self.assertEqual(len(h.units), 20)
        self.assertEqual(len(l.units), 20)
        self.assertEqual(len(m.units), 20)
        self.assertEqual(len(b.units), 60)

        for i in range(0, 20):
            self.assertTrue(isinstance(h.units[i], main.Hunter))
            self.assertTrue(isinstance(l.units[i], main.Lumberjack))
            self.assertTrue(isinstance(m.units[i], main.Miner))
            self.assertTrue(isinstance(b.units[i * 3], main.Swordsman))
            self.assertTrue(isinstance(b.units[i * 3 + 1], main.Archer))
            self.assertTrue(isinstance(b.units[i * 3 + 2], main.Horseman))

    def test_unit_kill(self):
        s = main.Swordsman(1, 1)
        a = main.Archer(1, 1)
        hr = main.Horseman(1, 1)
        l = main.Lumberjack(1, 1)
        m = main.Miner(1, 1)
        hn = main.Hunter(1, 1)
        s.destroy()
        a.destroy()
        hr.destroy()
        l.destroy()
        m.destroy()
        hn.destroy()
        self.assertTrue(s.dead)
        self.assertTrue(a.dead)
        self.assertTrue(hr.dead)
        self.assertTrue(l.dead)
        self.assertTrue(m.dead)
        self.assertTrue(hn.dead)

    def test_single_building(self):
        b = main.Barrack(1, 1)
        l = main.LumberjackHut(1, 1)
        m = main.MinerHut(1, 1)
        h = main.HuntersHut(1, 1)
        self.assertEqual(b, main.Barrack(10, 10))
        self.assertEqual(l, main.LumberjackHut(10, 10))
        self.assertEqual(m, main.MinerHut(10, 10))
        self.assertEqual(h, main.HuntersHut(10, 10))

    def test_building_destroy(self):
        b = main.Barrack(1, 1)
        l = main.LumberjackHut(1, 1)
        m = main.MinerHut(1, 1)
        h = main.HuntersHut(1, 1)
        b.destroy()
        l.destroy()
        m.destroy()
        h.destroy()
        self.assertNotEqual(b, main.Barrack(10, 10))
        self.assertNotEqual(l, main.LumberjackHut(10, 10))
        self.assertNotEqual(m, main.MinerHut(10, 10))
        self.assertNotEqual(h, main.HuntersHut(10, 10))


unittest.main()
