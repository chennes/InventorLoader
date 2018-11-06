# -*- coding: utf-8 -*-

'''
importerEeScene.py:
Simple approach to read/analyse Autodesk (R) Invetor (R) part file's (IPT) browser view data.
The importer can read files from Autodesk (R) Invetor (R) Inventro V2010 on. Older versions will fail!
'''

from importerSegment import SegmentReader, checkReadAll
from importerUtils   import *
import importerSegNode

__author__     = 'Jens M. Plonka'
__copyright__  = 'Copyright 2018, Germany'
__url__        = "https://www.github.com/jmplonka/InventorLoader"

class EeSceneReader(SegmentReader):
	def __init__(self, segment):
		super(EeSceneReader, self).__init__(segment)

	def Read_32RRR2(self, node, typeName = None):
		i = node.Read_Header0(typeName)
		i = node.ReadUInt32(i, 'index') # until 2019 this is always 0 otherwise it references the element with sketch's index in DC-Segment
		i = node.ReadChildRef(i, 'styles')
		i = node.ReadChildRef(i, 'ref_1')
		i = node.ReadParentRef(i)
		i = node.ReadUInt32(i, 'u32_0')
		i = self.skipBlockSize(i)
		return i

	def Read_ColorAttr(self, offset, node):
		i = self.skipBlockSize(offset)
		i = node.ReadUInt8A(i, 2, 'ColorAttr.a0')
		i = node.ReadColorRGBA(i, 'ColorAttr.c0')
		i = node.ReadColorRGBA(i, 'ColorAttr.c1')
		i = node.ReadColorRGBA(i, 'ColorAttr.c2')
		i = node.ReadColorRGBA(i, 'ColorAttr.c3')
		i = node.ReadUInt16A(i, 2, 'ColorAttr.a5')
		return i

	def Read_120284EF(self, node):
		i = self.ReadHeaderSU32S(node)
		i = node.ReadUInt8(i, 'u8_0')
		i = self.skipBlockSize(i)
		i = node.ReadList2(i, importerSegNode._TYP_NODE_REF_, 'lst0')
		return i

	def Read_13FC8170(self, node):
		i = self.ReadHeaderSU32S(node)
		i = node.ReadUInt8(i, 'u8_0')
		i = self.skipBlockSize(i)
		i = node.ReadUInt8(i, 'u8_1')
		return i

	def Read_48EB8607(self, node):
		node.typeName = "ObjctStyles"
		i = self.skipBlockSize(0)
		i = node.ReadList2(i, importerSegNode._TYP_NODE_REF_, 'styles')
		return i

	def Read_5194E9A3(self, node): # Surface
		i = self.Read_32RRR2(node, 'Surface')
		i = node.ReadList2(i, importerSegNode._TYP_NODE_REF_, 'lst0')
		i = node.ReadUInt8(i, 'u8_0')
		i = self.skipBlockSize(i, 8)
		i = node.ReadFloat64A(i, 3, 'a2')
		i = node.ReadFloat64A(i, 3, 'a3')
		i = self.skipBlockSize(i)
		i = node.ReadUInt32(i, 'index')
		i = node.ReadUInt32A(i, 2, 'a4')
		return i

	def Read_6C6322EB(self, node):
		i = self.ReadHeaderSU32S(node)
		i = node.ReadUInt8(i, 'u8_0')
		i = self.skipBlockSize(i)
		i = node.ReadUInt32(i, 'u32_1')
		i = node.ReadList2(i, importerSegNode._TYP_UINT32_, 'lst0')
		i = self.skipBlockSize(i)
		i = node.ReadUInt8(i, 'u8_1')
		i = self.skipBlockSize(i)
		return i

	def Read_950A4A74(self, node):
		i = node.ReadUInt32A(0, 3, 'a0')
		return i

	def Read_A529D1E2(self, node):
		i = self.ReadHeaderU32RefU8List3(node)
		return i

	def Read_A79EACCB(self, node):
		i = node.Read_Header0()
		i = node.ReadUInt32(i, 'flags')
		i = node.ReadChildRef(i, 'ref0')
		i = node.ReadUInt32(i, 'u32_0')
		i = node.ReadParentRef(i)
		i = node.ReadUInt32(i, 'u32_0')
		i = self.skipBlockSize(i)
		i = node.ReadList2(i, importerSegNode._TYP_FLOAT32_A_, 'lst0', 3)
		i = node.ReadUInt8(i, 'u8_0')
		return i

	def Read_A79EACCF(self, node): # 3dObject
		i = node.Read_Header0('3dObject')
		i = node.ReadUInt32(i, 'flags')
		i = node.ReadChildRef(i, 'styles')
		i = node.ReadChildRef(i, 'ref1')
		i = node.ReadCrossRef(i, 'ref2')
		i = node.ReadCrossRef(i, 'styles')
		i = self.skipBlockSize(i)
		i = node.ReadList2(i, importerSegNode._TYP_NODE_REF_, 'lst0')
		i = node.ReadUInt8(i, 'u8_0')
		return i

	def Read_A79EACD2(self, node):
		i = node.Read_Header0()
		i = node.ReadUInt32(i, 'flags')
		i = node.ReadChildRef(i, 'ref0')
		i = node.ReadChildRef(i, 'ref1')
		i = node.ReadParentRef(i)
		i = node.ReadCrossRef(i, 'styles')
		i = self.skipBlockSize(i)
		i = node.ReadList2(i, importerSegNode._TYP_FLOAT32_A_, 'lst0', 3)
		i = node.ReadList2(i, importerSegNode._TYP_UINT16_A_,  'lst1', 2)
		i = node.ReadList2(i, importerSegNode._TYP_FLOAT32_A_, 'lst2', 3)
		i = node.ReadList2(i, importerSegNode._TYP_FLOAT32_A_, 'lst3', 2)
		i = node.ReadUInt16A(i, 2, 'a0')
		i = node.ReadList2(i, importerSegNode._TYP_NODE_REF_, 'lst4')
		i = node.ReadFloat32_2D(i, 'a1')
		return i

	def Read_B32BF6A2(self, node):
		i = self.skipBlockSize(0)
		i = node.ReadUInt16(i, 'u16_0')
		i = self.Read_ColorAttr(i, node)
		i = self.skipBlockSize(i)
		return i

	def Read_B91E695F(self, node):
		i = node.Read_Header0()
		i = node.ReadUInt32A(i, 2, 'a0')
		i = node.ReadUInt8(i, 'u8_0')
		i = self.skipBlockSize(i)
		i = node.ReadUInt32A(i, 3, 'a1')
		i = node.ReadUInt8(i, 'u8_1')
		i = node.ReadUInt32A(i, 4, 'a2')
		i = node.ReadUInt16(i, 'u16_0')
		i = node.ReadUInt32A(i, 5, 'a3')
		i = node.ReadList2(i, importerSegNode._TYP_F64_F64_U32_U8_U8_U16_, 'lst0')
		i = self.skipBlockSize(i)
		i = node.ReadFloat64_2D(i, 'a4')
		i = self.skipBlockSize(i, 8)
		i = node.ReadUInt32(i, 'u32_0')
		return i

	def Read_48EB8608(self, node): #StyleLine2dColor
		i = self.ReadHeaderSU32S(node, 'StyleLine2dColor')
		i = node.ReadColorRGBA(i, 'c0')
		i = node.ReadColorRGBA(i, 'c1')
		i = node.ReadColorRGBA(i, 'c2')
		i = node.ReadColorRGBA(i, 'c3')
		i = node.ReadColorRGBA(i, 'c4')
		i = node.ReadUInt32(i, 'u32_1')
		i = self.skipBlockSize(i)
		i = node.ReadUInt8(i, 'u8_0')
		return i

	def Read_6E176BB6(self, node): # Object style ...
		i = self.ReadHeaderSU32S(node, 'Style_B32BF6A7')
		i = node.ReadFloat64(i, 'f64_0')
		i = node.ReadFloat64_3D(i, 'vec')
		i = node.ReadFloat64(i, 'f64_1')
		i = node.ReadUInt32(i, 'u32_1')
		return i

	def Read_7AE0E1A3(self, node): # Object style ...
		i = self.ReadHeaderSU32S(node, 'Style_7AE0E1A3')
		i = node.ReadFloat64_2D(i, 'a0')
		return i

	def Read_8F0B160B(self, node): # Object style ...
		i = self.ReadHeaderSU32S(node, 'Style_8F0B160B')
		i = node.ReadColorRGBA(i, 'c0')
		i = node.ReadColorRGBA(i, 'c1')
		i = node.ReadColorRGBA(i, 'c2')
		i = node.ReadColorRGBA(i, 'c3')
		i = node.ReadColorRGBA(i, 'c4')
		i = node.ReadUInt16A(i, 2, 'a10')
		i = self.skipBlockSize(i)
		i = node.ReadUInt8(i, 'u8_0')
		i = self.skipBlockSize(i)
		i = node.ReadUInt16A(i, 10, 'a11')
		return i

	def Read_8F0B160C(self, node): # Object style ...
		i = self.ReadHeaderSU32S(node, 'Style_8F0B160C')
		i = node.ReadUInt16A(i, 10, 'a0')
		i = node.ReadUInt8(i, 'u8_0')
		i = node.ReadUInt16A(i, 3, 'a1')
		i = self.skipBlockSize(i)
		i = node.ReadUInt16A(i, 4, 'a2')
		i = self.skipBlockSize(i)
		i = node.ReadUInt32(i, 'u32_1')
		return i

	def Read_9795E56A(self, node): # Object style ...
		i = self.ReadHeaderSU32S(node, 'Style_9795E56A')
		i = node.ReadFloat64_3D(i, 'a1')
		return i

	def Read_AF48560F(self, node): # ColorStylePrimAttr
		i = self.ReadHeaderSU32S(node, 'PrimColorAttr')
		i = node.ReadUInt16A(i, 7, 'a0')
		i = self.Read_ColorAttr(i, node)
		i = self.skipBlockSize(i)
		i = node.ReadUInt8(i, 'u8_0')
		i = node.ReadUInt16A(i, 2, 'a1')
		i = self.skipBlockSize(i)
		i = node.ReadUInt8(i, 'u8_1')
		return i

	def Read_B255D907(self, node): # Object style ...
		i = self.ReadHeaderSU32S(node, 'Style_B255D907')
		i = node.ReadFloat64_3D(i, 'a0')
		return i

	def Read_B32BF6A3(self, node): # visibility style
		i = self.ReadHeaderSU32S(node, 'StyleVisibility')
		i = node.ReadBoolean(i, 'visible')
		return i

	def Read_B32BF6A5(self, node): # Object style ...
		i = self.ReadHeaderSU32S(node, 'Style_B32BF6A5')
		i = node.ReadUInt16(i, 'u16_0')
		return i

	def Read_B32BF6A6(self, node): # Object style ...
		i = self.ReadHeaderSU32S(node, 'Style_B32BF6A6')
		i = node.ReadUInt8(i, 'u8_0')
		return i

	def Read_B32BF6A7(self, node): # Object style ...
		i = self.ReadHeaderSU32S(node, 'Style_B32BF6A7')
		i = node.ReadFloat64(i, 'f64_0')
		i = node.ReadFloat64_3D(i, 'vec')
		i = node.ReadFloat64(i, 'f64_1')
		i = node.ReadUInt32(i, 'u32_1')
		return i

	def Read_B32BF6A9(self, node): # Object style ...
		i = self.ReadHeaderSU32S(node, 'Style_B32BF6A9')
		i = node.ReadUInt16(i, 'u16_0')
		return i

	def Read_B32BF6AB(self, node): # Object style ...
		i = self.ReadHeaderSU32S(node, 'Style_B32BF6AB')
		i = node.ReadUInt8(i, 'u8_0')
		return i

	def Read_B32BF6AC(self, node): # line style
		i = self.ReadHeaderSU32S(node, 'StyleLine')
		i = node.ReadUInt16(i, 'u16_0')
		i = node.ReadFloat32(i, 'width')
		i = node.ReadUInt16A(i, 2, 'a0')
		i = node.ReadUInt8(i, 'u8_0')
		i = node.ReadUInt16(i, 'u16_1')
		cnt, i = getUInt16(node.data, i)
		a1 = []
		for j in range(cnt):
			u, i = getUInt32(node.data, i)
			f, i = getFloat32(node.data, i)
			a1.append((u, f))
		node.content += u" a1=[%s]" %(u",".join(["(%04X,%g)" %(x[0], x[1]) for x in a1]))
		node.set('a1', a1)
		i = node.ReadFloat32_3D(i, 'a2')
		i = self.skipBlockSize(i)
		i = node.ReadUInt16A(i, 4, 'a3')
		return i

	def Read_C29D5C11(self, node): # Object style ...
		i = self.ReadHeaderSU32S(node, 'Style_C29D5C11')
		i = node.ReadFloat64_3D(i, 'a0')
		return i
