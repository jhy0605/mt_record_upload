/*******************************************************************************
 * Copyright (c) 2018, 2021 IBM Corp. and others
 *
 * This program and the accompanying materials are made available under
 * the terms of the Eclipse Public License 2.0 which accompanies this
 * distribution and is available at https://www.eclipse.org/legal/epl-2.0/
 * or the Apache License, Version 2.0 which accompanies this distribution and
 * is available at https://www.apache.org/licenses/LICENSE-2.0.
 *
 * This Source Code may also be made available under the following
 * Secondary Licenses when the conditions for such availability set
 * forth in the Eclipse Public License, v. 2.0 are satisfied: GNU
 * General Public License, version 2 with the GNU Classpath
 * Exception [1] and GNU General Public License, version 2 with the
 * OpenJDK Assembly Exception [2].
 *
 * [1] https://www.gnu.org/software/classpath/license.html
 * [2] http://openjdk.java.net/legal/assembly-exception.html
 *
 * SPDX-License-Identifier: EPL-2.0 OR Apache-2.0 OR GPL-2.0 WITH Classpath-exception-2.0 OR LicenseRef-GPL-2.0 WITH Assembly-exception
 *******************************************************************************/
package openj9.lang.management.internal;

import javax.management.MalformedObjectNameException;
import javax.management.ObjectName;
import com.ibm.jvm.Dump;
import com.ibm.jvm.DumpConfigurationUnavailableException;
import com.ibm.jvm.InvalidDumpOptionException;
import com.ibm.java.lang.management.internal.ManagementPermissionHelper;

import openj9.lang.management.ConfigurationUnavailableException;
import openj9.lang.management.InvalidOptionException;
import openj9.lang.management.OpenJ9DiagnosticsMXBean;

/**
 * Runtime type for {@link OpenJ9DiagnosticsMXBean}.
 * <p>
 * Implements functionality to dynamically configure dump options and to trigger supported dump agents.
 * </p>
 */
public final class OpenJ9DiagnosticsMXBeanImpl implements OpenJ9DiagnosticsMXBean {

	private static final OpenJ9DiagnosticsMXBean instance = createInstance();

	private static OpenJ9DiagnosticsMXBean createInstance() {
		return new OpenJ9DiagnosticsMXBeanImpl();
	}

	/**
	 * {@inheritDoc}
	 */
	@Override
	public void resetDumpOptions() throws ConfigurationUnavailableException {
		checkManagementSecurityPermission();
		try {
			Dump.resetDumpOptions();
		} catch (Exception e) {
			handleDumpConfigurationUnavailableException(e);
			throw handleError(e);
		}
	}

	/**
	 * {@inheritDoc}
	 */
	@Override
	public String[] queryDumpOptions() {
		checkManagementSecurityPermission();
		try {
			return Dump.queryDumpOptions();
		} catch (Exception e) {
			throw handleError(e);
		}
	}

	/**
	 * {@inheritDoc}
	 */
	@Override
	public void setDumpOptions(String dumpOptions) throws InvalidOptionException, ConfigurationUnavailableException {
		checkManagementSecurityPermission();
		try {
			Dump.setDumpOptions(dumpOptions);
		} catch (Exception e) {
			handleInvalidDumpOptionException(e);
			handleDumpConfigurationUnavailableException(e);
			throw handleError(e);
		}
	}

	/**
	 * {@inheritDoc}
	 */
	@Override
	public void triggerDump(String dumpAgent) throws IllegalArgumentException {
		checkManagementSecurityPermission();
		switch (dumpAgent) {
		case "java": //$NON-NLS-1$
			Dump.JavaDump();
			break;
		case "heap": //$NON-NLS-1$
			Dump.HeapDump();
			break;
		case "system": //$NON-NLS-1$
			Dump.SystemDump();
			break;
		case "snap": //$NON-NLS-1$
			Dump.SnapDump();
			break;
		default:
			// K0663 = Invalid or Unsupported Dump Agent cannot be triggered
			throw new IllegalArgumentException(com.ibm.oti.util.Msg.getString("K0663")); //$NON-NLS-1$
		}
	}

	/**
	 * {@inheritDoc}
	 */
	@Override
	public String triggerDumpToFile(String dumpAgent, String fileNamePattern) throws IllegalArgumentException, InvalidOptionException {
		String fileName = null;
		checkManagementSecurityPermission();
		switch (dumpAgent) {
		case "java": //$NON-NLS-1$
			try {
				fileName = Dump.javaDumpToFile(fileNamePattern);
			} catch (Exception e) {
				handleInvalidDumpOptionException(e);
				throw handleError(e);
			}
			break;
		case "heap": //$NON-NLS-1$
			try {
				fileName = Dump.heapDumpToFile(fileNamePattern);
			} catch (Exception e) {
				handleInvalidDumpOptionException(e);
				throw handleError(e);
			}
			break;
		case "system": //$NON-NLS-1$
			try {
				fileName = Dump.systemDumpToFile(fileNamePattern);
			} catch (Exception e) {
				handleInvalidDumpOptionException(e);
				throw handleError(e);
			}
			break;
		case "snap": //$NON-NLS-1$
			try {
				fileName = Dump.snapDumpToFile(fileNamePattern);
			} catch (Exception e) {
				handleInvalidDumpOptionException(e);
				throw handleError(e);
			}
			break;
		default:
			// K0663 = Invalid or Unsupported Dump Agent cannot be triggered
			throw new IllegalArgumentException(com.ibm.oti.util.Msg.getString("K0663")); //$NON-NLS-1$
		}
		return fileName;
	}

	/**
	 * {@inheritDoc}
	 */
	@Override
	public String triggerClassicHeapDump() throws InvalidOptionException {
		String dumpOptions = "heap:opts=CLASSIC"; //$NON-NLS-1$
		checkManagementSecurityPermission();
		try {
			String fileName = Dump.triggerDump(dumpOptions);
			return fileName;
		} catch (Exception e) {
			handleInvalidDumpOptionException(e);
			throw handleError(e);
		}
	}

	private static void checkManagementSecurityPermission() {
		/* Check the caller has Management Permission. */
		@SuppressWarnings("removal")
		SecurityManager manager = System.getSecurityManager();
		if (manager != null) {
			manager.checkPermission(ManagementPermissionHelper.MPCONTROL);
		}
	}

	/**
	 * Singleton accessor method. Returns an instance of {@link OpenJ9DiagnosticsMXBeanImpl}.
	 *
	 * @return a static instance of {@link OpenJ9DiagnosticsMXBeanImpl}.
	 */
	public static OpenJ9DiagnosticsMXBean getInstance() {
		return instance;
	}

	/**
	 * Private constructor to prevent instantiation by others.
	 */
	private OpenJ9DiagnosticsMXBeanImpl() {
		super();
	}

	/**
	 * Returns the object name of the MXBean.
	 *
	 * @return objectName representing the MXBean.
	 */
	@Override
	public ObjectName getObjectName() {
		try {
			return ObjectName.getInstance("openj9.lang.management:type=OpenJ9Diagnostics"); //$NON-NLS-1$
		} catch (MalformedObjectNameException e) {
			throw new InternalError(e);
		}
	}

	/* Handle error thrown by method invoke as internal error */
	private static InternalError handleError(Exception error) {
		throw new InternalError(error.toString(), error);
	}

	private void handleInvalidDumpOptionException(Exception cause) throws InvalidOptionException {
		if (cause instanceof InvalidDumpOptionException) {
			throw new InvalidOptionException("Error in dump options specified", cause); //$NON-NLS-1$
		}
	}

	private void handleDumpConfigurationUnavailableException(Exception cause) throws ConfigurationUnavailableException {
		if (cause instanceof DumpConfigurationUnavailableException) {
			throw new ConfigurationUnavailableException("Dump configuration cannot be changed while a dump is in progress", cause); //$NON-NLS-1$
		}
	}

}
