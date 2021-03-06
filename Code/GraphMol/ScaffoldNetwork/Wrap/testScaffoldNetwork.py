#
# Copyright (C) 2019 Greg Landrum and T5 Informatics GmbH
#  All Rights Reserved
#
#  This file is part of the RDKit.
#  The contents are covered by the terms of the BSD license
#  which is included in the file license.txt, found at the root
#  of the RDKit source tree.
#

import unittest
from rdkit import Chem
from rdkit.Chem.Scaffolds import rdScaffoldNetwork
from rdkit import RDConfig
from rdkit import rdBase
import pickle
rdBase.DisableLog("rdApp.info")


class TestCase(unittest.TestCase):

  def setUp(self):
    pass

  def test1Basics(self):
    smis = ["c1ccccc1CC1NC(=O)CCC1", "c1cccnc1CC1NC(=O)CCC1"]
    ms = [Chem.MolFromSmiles(x) for x in smis]
    params = rdScaffoldNetwork.ScaffoldNetworkParams()

    net = rdScaffoldNetwork.CreateScaffoldNetwork(ms, params)
    self.assertEqual(len(net.nodes), 12)
    self.assertEqual(len(net.edges), 12)
    self.assertEqual(len(net.counts), len(net.nodes))
    self.assertEqual(len([x for x in net.edges if x.type == rdScaffoldNetwork.EdgeType.Fragment]),
                     4)
    self.assertEqual(len([x for x in net.edges if x.type == rdScaffoldNetwork.EdgeType.Generic]), 3)
    self.assertEqual(
      len([x for x in net.edges if x.type == rdScaffoldNetwork.EdgeType.RemoveAttachment]), 5)

    net = rdScaffoldNetwork.ScaffoldNetwork()
    rdScaffoldNetwork.UpdateScaffoldNetwork(ms, net, params)
    self.assertEqual(len(net.nodes), 12)
    self.assertEqual(len(net.edges), 12)
    self.assertEqual(len([x for x in net.edges if x.type == rdScaffoldNetwork.EdgeType.Fragment]),
                     4)
    self.assertEqual(len([x for x in net.edges if x.type == rdScaffoldNetwork.EdgeType.Generic]), 3)
    self.assertEqual(
      len([x for x in net.edges if x.type == rdScaffoldNetwork.EdgeType.RemoveAttachment]), 5)

  def test2Basics(self):
    smis = ["c1ccccc1CC1NC(=O)CCC1", "c1cccnc1CC1NC(=O)CCC1"]
    ms = [Chem.MolFromSmiles(x) for x in smis]
    params = rdScaffoldNetwork.ScaffoldNetworkParams()
    params.includeScaffoldsWithoutAttachments = False
    net = rdScaffoldNetwork.CreateScaffoldNetwork(ms, params)
    self.assertEqual(len(net.nodes), 7)
    self.assertEqual(len(net.edges), 7)
    self.assertEqual(len([x for x in net.edges if x.type == rdScaffoldNetwork.EdgeType.Fragment]),
                     4)
    self.assertEqual(len([x for x in net.edges if x.type == rdScaffoldNetwork.EdgeType.Generic]), 3)

  def test3Update(self):
    smis = ["c1ccccc1CC1NC(=O)CCC1", "c1cccnc1CC1NC(=O)CCC1"]
    ms = [Chem.MolFromSmiles(x) for x in smis]
    params = rdScaffoldNetwork.ScaffoldNetworkParams()
    net = rdScaffoldNetwork.ScaffoldNetwork()
    rdScaffoldNetwork.UpdateScaffoldNetwork(ms[0:1], net, params)
    self.assertEqual(len(net.nodes), 9)
    self.assertEqual(len(net.edges), 8)
    self.assertEqual(len(net.counts), len(net.nodes))
    self.assertEqual(list(net.counts).count(1), len(net.counts))
    rdScaffoldNetwork.UpdateScaffoldNetwork(ms[1:2], net, params)
    self.assertEqual(len(net.nodes), 12)
    self.assertEqual(len(net.edges), 12)
    self.assertEqual(len(net.counts), len(net.nodes))
    self.assertEqual(len([x for x in net.edges if x.type == rdScaffoldNetwork.EdgeType.Fragment]),
                     4)
    self.assertEqual(len([x for x in net.edges if x.type == rdScaffoldNetwork.EdgeType.Generic]), 3)
    self.assertEqual(
      len([x for x in net.edges if x.type == rdScaffoldNetwork.EdgeType.RemoveAttachment]), 5)

    net = rdScaffoldNetwork.CreateScaffoldNetwork(ms[0:1], params)
    rdScaffoldNetwork.UpdateScaffoldNetwork(ms[1:2], net, params)
    self.assertEqual(len(net.nodes), 12)
    self.assertEqual(len(net.edges), 12)
    self.assertEqual(len([x for x in net.edges if x.type == rdScaffoldNetwork.EdgeType.Fragment]),
                     4)
    self.assertEqual(len([x for x in net.edges if x.type == rdScaffoldNetwork.EdgeType.Generic]), 3)
    self.assertEqual(
      len([x for x in net.edges if x.type == rdScaffoldNetwork.EdgeType.RemoveAttachment]), 5)

  def test4Str(self):
    smis = ["c1ccccc1CC1NC(=O)CCC1"]
    ms = [Chem.MolFromSmiles(x) for x in smis]
    params = rdScaffoldNetwork.ScaffoldNetworkParams()

    net = rdScaffoldNetwork.CreateScaffoldNetwork(ms, params)
    self.assertEqual(len(net.nodes), 9)
    self.assertEqual(len(net.edges), 8)
    self.assertEqual(str(net.edges[0]), "NetworkEdge( 0->1, type:Fragment )")

  def test5Pickle(self):
    smis = ["c1ccccc1CC1NC(=O)CCC1", "c1cccnc1CC1NC(=O)CCC1"]
    ms = [Chem.MolFromSmiles(x) for x in smis]
    params = rdScaffoldNetwork.ScaffoldNetworkParams()
    params.includeScaffoldsWithoutAttachments = False
    net = rdScaffoldNetwork.CreateScaffoldNetwork(ms, params)
    self.assertEqual(len(net.nodes), 7)
    self.assertEqual(len(net.edges), 7)

    pkl = pickle.dumps(net)
    net2 = pickle.loads(pkl)
    self.assertEqual(len(net2.nodes), 7)
    self.assertEqual(len(net2.edges), 7)
    self.assertEqual(list(net2.nodes), list(net.nodes))
    self.assertEqual([str(x) for x in net2.edges], [str(x) for x in net.edges])

  def test6FragmentationReactions(self):
    smis = ["c1c(CC2CC2)cc(NC2CC2)cc1OC1CC1"]
    ms = [Chem.MolFromSmiles(x) for x in smis]
    params = rdScaffoldNetwork.ScaffoldNetworkParams(
      ["[!#0;R:1]-!@[O:2]>>[*:1]-[#0].[#0]-[*:2]", "[!#0;R:1]-!@[N:2]>>[*:1]-[#0].[#0]-[*:2]"])
    params.includeScaffoldsWithoutAttachments = False
    params.includeGenericScaffolds = False
    net = rdScaffoldNetwork.CreateScaffoldNetwork(ms, params)
    self.assertEqual(len(net.nodes), 5)
    self.assertEqual(len(net.edges), 7)


if __name__ == '__main__':
  unittest.main()
