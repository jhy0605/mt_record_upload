/*===========================================================================
 * Licensed Materials - Property of IBM
 * "Restricted Materials of IBM"
 * 
 * IBM SDK, Java(tm) Technology Edition, v8
 * (C) Copyright IBM Corp. 2009, 2017. All Rights Reserved
 *
 * US Government Users Restricted Rights - Use, duplication or disclosure
 * restricted by GSA ADP Schedule Contract with IBM Corp.
 *===========================================================================
 */
/*
 * Copyright (c) 2009, 2011, Oracle and/or its affiliates. All rights reserved.
 * ORACLE PROPRIETARY/CONFIDENTIAL. Use is subject to license terms.
 *
 *
 *
 *
 *
 *
 *
 *
 *
 *
 *
 *
 *
 *
 *
 *
 *
 *
 *
 *
 */

package java.util.zip;

import java.nio.ByteBuffer;
import java.nio.CharBuffer;
import java.nio.charset.Charset;
import java.nio.charset.StandardCharsets;
import java.nio.charset.CharsetDecoder;
import java.nio.charset.CharsetEncoder;
import java.nio.charset.CoderResult;
import java.nio.charset.CodingErrorAction;
import java.util.Arrays;
import sun.nio.cs.ArrayDecoder;
import sun.nio.cs.ArrayEncoder;
import com.ibm.jvm.MemorySafetyService;                                         //IBM-T6_wrt_bringup
/**
 * Utility class for zipfile name and comment decoding and encoding
 */

final class ZipCoder {

    String toString(byte[] ba, int length) {
        CharsetDecoder cd = decoder().reset();
        int len = (int)(length * cd.maxCharsPerByte());
        char[] ca = new char[len];
        if (len == 0)
            return new String(ca);
        // UTF-8 only for now. Other ArrayDeocder only handles
        // CodingErrorAction.REPLACE mode. ZipCoder uses
        // REPORT mode.
        if (isUTF8 && cd instanceof ArrayDecoder) {
            int clen = ((ArrayDecoder)cd).decode(ba, 0, length, ca);
            if (clen == -1)    // malformed
                throw new IllegalArgumentException("MALFORMED");
            return new String(ca, 0, clen);
        }
        ByteBuffer bb = ByteBuffer.wrap(ba, 0, length);
        CharBuffer cb = CharBuffer.wrap(ca);
        CoderResult cr = cd.decode(bb, cb, true);
        if (!cr.isUnderflow())
            throw new IllegalArgumentException(cr.toString());
        cr = cd.flush(cb);
        if (!cr.isUnderflow())
            throw new IllegalArgumentException(cr.toString());
        return new String(ca, 0, cb.position());
    }

    String toString(byte[] ba) {
        return toString(ba, ba.length);
    }

    byte[] getBytes(String s) {
        CharsetEncoder ce = encoder().reset();
        char[] ca = s.toCharArray();
        int len = (int)(ca.length * ce.maxBytesPerChar());
        byte[] ba = new byte[len];
        if (len == 0)
            return ba;
        // UTF-8 only for now. Other ArrayDeocder only handles
        // CodingErrorAction.REPLACE mode.
        if (isUTF8 && ce instanceof ArrayEncoder) {
            int blen = ((ArrayEncoder)ce).encode(ca, 0, ca.length, ba);
            if (blen == -1)    // malformed
                throw new IllegalArgumentException("MALFORMED");
            return Arrays.copyOf(ba, blen);
        }
        ByteBuffer bb = ByteBuffer.wrap(ba);
        CharBuffer cb = CharBuffer.wrap(ca);
        CoderResult cr = ce.encode(cb, bb, true);
        if (!cr.isUnderflow())
            throw new IllegalArgumentException(cr.toString());
        cr = ce.flush(bb);
        if (!cr.isUnderflow())
            throw new IllegalArgumentException(cr.toString());
        if (bb.position() == ba.length)  // defensive copy?
            return ba;
        else
            return Arrays.copyOf(ba, bb.position());
    }

    // assume invoked only if "this" is not utf8
    byte[] getBytesUTF8(String s) {
        if (isUTF8)
            return getBytes(s);
        if (utf8 == null)
            utf8 = new ZipCoder(StandardCharsets.UTF_8);
        return utf8.getBytes(s);
    }


    String toStringUTF8(byte[] ba, int len) {
        if (isUTF8)
            return toString(ba, len);
        if (utf8 == null)
            utf8 = new ZipCoder(StandardCharsets.UTF_8);
        return utf8.toString(ba, len);
    }

    boolean isUTF8() {
        return isUTF8;
    }

    private Charset cs;
    private CharsetDecoder dec;
    private CharsetEncoder enc;
    private boolean isUTF8;
    private ZipCoder utf8;

    private ZipCoder(Charset cs) {
        this.cs = cs;
        this.isUTF8 = cs.name().equals(StandardCharsets.UTF_8.name());
    }

    static ZipCoder get(Charset charset) {
        return new ZipCoder(charset);
    }

    private CharsetDecoder decoder() {
        if (dec == null) {
               long oldMemory = -1;                                            //IBM-T6_wrt_bringup
                try                                                            //IBM-T6_wrt_bringup
                {                                                              //IBM-T6_wrt_bringup
                    oldMemory = MemorySafetyService.enterSafeMemoryArea();     //IBM-T6_wrt_bringup
                    dec = cs.newDecoder()
                    .onMalformedInput(CodingErrorAction.REPORT)
                    .onUnmappableCharacter(CodingErrorAction.REPORT);
                 }                                                               //IBM-T6_wrt_bringup
                finally                                                         //IBM-T6_wrt_bringup
                {                                                               //IBM-T6_wrt_bringup
                        MemorySafetyService.exitLastMemoryArea(oldMemory);      //IBM-T6_wrt_bringup
                }                                                               //IBM-T6_wrt_bringup
                                                                                //IBM-T6_wrt_bringup
        }
        return dec;
    }

    private CharsetEncoder encoder() {
        if (enc == null) {
        	long oldMemory = -1;                                            //IBM-T6_wrt_bringup
		try                                                             //IBM-T6_wrt_bringup
		{                                                               //IBM-T6_wrt_bringup
			oldMemory = MemorySafetyService.enterSafeMemoryArea();  //IBM-T6_wrt_bringup
			enc = cs.newEncoder()                                   //IBM-T6_wrt_bringup
	             	.onMalformedInput(CodingErrorAction.REPORT)        //IBM-T6_wrt_bringup
	             	.onUnmappableCharacter(CodingErrorAction.REPORT);  //IBM-T6_wrt_bringup
		}                                                               //IBM-T6_wrt_bringup
		finally                                                         //IBM-T6_wrt_bringup
		{                                                               //IBM-T6_wrt_bringup
			MemorySafetyService.exitLastMemoryArea(oldMemory);      //IBM-T6_wrt_bringup
		}                                                               //IBM-T6_wrt_bringup
                                                                                //IBM-T6_wrt_bringup
        }
        return enc;
    }
}
//IBM-T6_wrt_bringup
