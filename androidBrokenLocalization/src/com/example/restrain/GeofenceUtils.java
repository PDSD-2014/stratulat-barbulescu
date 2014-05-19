/*
 * Copyright (C) 2013 The Android Open Source Project
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package com.example.restrain;

public final class GeofenceUtils {

    public enum REMOVE_TYPE {INTENT, LIST}

    public enum REQUEST_TYPE {ADD, REMOVE}

    public static final String APPTAG = "Geofence Detection";

    public static final String ACTION_CONNECTION_ERROR          = "com.example.restrain.ACTION_CONNECTION_ERROR";
    public static final String ACTION_CONNECTION_SUCCESS        = "com.example.restrain.ACTION_CONNECTION_SUCCESS";
    public static final String ACTION_GEOFENCES_ADDED           = "com.example.restrain.ACTION_GEOFENCES_ADDED";
    public static final String ACTION_GEOFENCES_REMOVED         = "com.example.restrain.ACTION_GEOFENCES_DELETED";
    public static final String ACTION_GEOFENCE_ERROR            = "com.example.restrain.ACTION_GEOFENCES_ERROR";
    public static final String ACTION_GEOFENCE_TRANSITION       = "com.example.restrain.ACTION_GEOFENCE_TRANSITION";
    public static final String ACTION_GEOFENCE_TRANSITION_ERROR = "com.example.restrain.ACTION_GEOFENCE_TRANSITION_ERROR";
    public static final String CATEGORY_LOCATION_SERVICES       = "com.example.restrain.CATEGORY_LOCATION_SERVICES";

    // Keys for extended data in Intents
    public static final String EXTRA_CONNECTION_CODE = "com.restrain.EXTRA_CONNECTION_CODE";

    public static final String EXTRA_CONNECTION_ERROR_CODE =
            "com.example.android.geofence.EXTRA_CONNECTION_ERROR_CODE";

    public static final String EXTRA_CONNECTION_ERROR_MESSAGE =
            "com.example.android.geofence.EXTRA_CONNECTION_ERROR_MESSAGE";

    public static final String EXTRA_GEOFENCE_STATUS =
            "com.example.android.geofence.EXTRA_GEOFENCE_STATUS";

    public static final String KEY_LATITUDE = "com.example.android.geofence.KEY_LATITUDE";

    public static final String KEY_LONGITUDE = "com.example.android.geofence.KEY_LONGITUDE";

    public static final String KEY_RADIUS = "com.example.android.geofence.KEY_RADIUS";

    public static final String KEY_EXPIRATION_DURATION =
            "com.example.android.geofence.KEY_EXPIRATION_DURATION";

    public static final String KEY_TRANSITION_TYPE =
            "com.example.android.geofence.KEY_TRANSITION_TYPE";

    public static final String KEY_PREFIX =
            "com.example.android.geofence.KEY";

    public static final long INVALID_LONG_VALUE = -999l;
    public static final float INVALID_FLOAT_VALUE = -999.0f;
    public static final int INVALID_INT_VALUE = -999;

    public static final double MAX_LATITUDE = 90.d;
    public static final double MIN_LATITUDE = -90.d;
    public static final double MAX_LONGITUDE = 180.d;
    public static final double MIN_LONGITUDE = -180.d;

    public static final float MIN_RADIUS = 1f;

    public final static int CONNECTION_FAILURE_RESOLUTION_REQUEST = 9000;
    public static final String EMPTY_STRING = new String();
    public static final CharSequence GEOFENCE_ID_DELIMITER = ",";
}