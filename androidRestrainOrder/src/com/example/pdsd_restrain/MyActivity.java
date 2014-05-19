package com.example.pdsd_restrain;

import android.app.Activity;
import android.app.PendingIntent;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.location.*;
import android.os.Bundle;
import android.os.Vibrator;
import android.util.Log;
import android.widget.TextView;
import android.widget.Toast;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.text.DecimalFormat;
import java.text.NumberFormat;

public class MyActivity extends Activity {
    private TextView latitudeField;
    private TextView longitudeField;
    private TextView colorIndicator;

    private LocationManager locationManager;
    private static final NumberFormat nf = new DecimalFormat("##.########");
    private static final String PROX_ALERT_INTENT_WARN = "com.example.pdsd-restrain.alert-warn";
    private static final float WARN_RADIUS = 3000;
    private static final String PROX_ALERT_INTENT_TRIG = "com.example.pdsd-restrain.alert-trig";
    private static final float TRIG_RADIUS = 10000;
    private static final int min_update = 1000; // should be 60000 in production
    private static final String AvoidanceListURL = "http://pastebin.com/raw.php?i=w2p2myfC";
    private double t_long;
    private double t_lat;

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main);
        latitudeField = (TextView) findViewById(R.id.TextView02);
        longitudeField = (TextView) findViewById(R.id.TextView04);
        colorIndicator = (TextView) findViewById(R.id.colour);
        colorIndicator.setBackgroundColor(getResources().getColor(R.color.invalid));

        Log.d("App", "Loading...");
        locationManager = (LocationManager) getSystemService(Context.LOCATION_SERVICE);

        Log.d("Location", "Available: " + locationManager.getAllProviders().toString());

        populateCoordinatesFromLastKnownLocation();

        // enable continous updates
        locationManager.requestLocationUpdates(LocationManager.GPS_PROVIDER, min_update, 0, new MyLocationListener());

        CoordGetter c = new CoordGetter();
        c.run();
        try {
            c.join();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        addProximityAlert(t_lat, t_long);
    }

    private void populateCoordinatesFromLastKnownLocation() {
        Location location = locationManager.getLastKnownLocation(LocationManager.GPS_PROVIDER);
        if (location!=null) {
            latitudeField.setText(nf.format(location.getLatitude()));
            longitudeField.setText(nf.format(location.getLongitude()));
        }else{
            latitudeField.setText("Unknown location");
            longitudeField.setText("Unknown location");
        }
    }

    // display continous updates
    public class MyLocationListener implements LocationListener {
        public void onLocationChanged(Location location) {
            Log.v("Location", location.toString());
            longitudeField.setText(nf.format(location.getLongitude()));
            latitudeField.setText(nf.format(location.getLatitude()));

            if( colorIndicator.getBackground().equals(getResources().getColor(R.color.invalid))){
                float dist[] = new float[1];
                Location.distanceBetween(location.getLatitude(), location.getLongitude(), t_lat, t_long, dist);
                if (dist[0] > WARN_RADIUS){
                    colorIndicator.setBackgroundColor(getResources().getColor(R.color.safe));
                }else if (dist[0] > TRIG_RADIUS) {
                    colorIndicator.setBackgroundColor(getResources().getColor(R.color.warn));
                }else{
                    colorIndicator.setBackgroundColor(getResources().getColor(R.color.trig));
                }
            }
        }

        public void onStatusChanged(String s, int i, Bundle b) {}
        public void onProviderDisabled(String s) {}
        public void onProviderEnabled(String s) {}
    }

    // get "interrupts"
    private void addProximityAlert(double latitude, double longitude) {
        Intent intent_t = new Intent(PROX_ALERT_INTENT_TRIG);
        Intent intent_w = new Intent(PROX_ALERT_INTENT_WARN);

        PendingIntent proximityIntent_t = PendingIntent.getBroadcast(this, 0, intent_t, 0);
        PendingIntent proximityIntent_w = PendingIntent.getBroadcast(this, 0, intent_w, 0);

        locationManager.addProximityAlert(latitude, longitude, TRIG_RADIUS, -1, proximityIntent_t);
        locationManager.addProximityAlert(latitude, longitude, WARN_RADIUS, -1, proximityIntent_w);

        IntentFilter filter_t = new IntentFilter(PROX_ALERT_INTENT_TRIG);
        registerReceiver(new ProximityIntentReceiver(0), filter_t);

        IntentFilter filter_w = new IntentFilter(PROX_ALERT_INTENT_WARN);
        registerReceiver(new ProximityIntentReceiver(1), filter_w);
    }

    public class ProximityIntentReceiver extends BroadcastReceiver{
        private int type;
        private Vibrator v;
        /*
         * type == 0 -> WARN
         * type == 1 -> TRIG
         */

        public ProximityIntentReceiver(int type){
            super();
            this.type = type;
            v = (Vibrator) getSystemService(Context.VIBRATOR_SERVICE);
        }

        @Override
        public void onReceive(Context context, Intent intent) {
            Boolean entering = intent.getBooleanExtra(LocationManager.KEY_PROXIMITY_ENTERING, false);

            if (type == 0){
                if(entering){
                    Toast.makeText(MyActivity.this, R.string.msg_enter_warn, Toast.LENGTH_LONG).show();
                    Log.d("Location", "enabled warning");
                    colorIndicator.setBackgroundColor(getResources().getColor(R.color.warn));
                    v.vibrate(1000);
               }else {
                   Toast.makeText(MyActivity.this, R.string.msg_exit_warn, Toast.LENGTH_LONG).show();
                    colorIndicator.setBackgroundColor(getResources().getColor(R.color.safe));
                    Log.d("Location", "disabled warning");
                    v.vibrate(500);
               }
            } else if(type == 1){
                if(entering){
                    Toast.makeText(MyActivity.this, R.string.msg_enter_trigger , Toast.LENGTH_LONG).show();
                    colorIndicator.setBackgroundColor(getResources().getColor(R.color.trig));
                    Log.d("Location", "enabled trigger");
                    v.vibrate(2000);
                }else {
                    Toast.makeText(MyActivity.this, R.string.msg_exit_trigger, Toast.LENGTH_LONG).show();
                    colorIndicator.setBackgroundColor(getResources().getColor(R.color.warn));
                    Log.d("Location", "disabled trigger");
                    v.vibrate(1000);
                }
            }
        }
    }

    public class CoordGetter extends Thread{
        public void run( ) {
            try {
                URL url = new URL(AvoidanceListURL);
                HttpURLConnection con = (HttpURLConnection) url.openConnection();
                readStream(con.getInputStream());
            } catch (Exception e) {
                e.printStackTrace();
            }
        }

        private void readStream(InputStream in) {
            BufferedReader reader = null;
            StringBuilder buffer = new StringBuilder();

            try {
                reader = new BufferedReader(new InputStreamReader(in));
                String line = "";
                while ((line = reader.readLine()) != null) {
                    buffer.append(line);
                }
            } catch (IOException e) {
                e.printStackTrace();
            } finally {
                if (reader != null) {
                    try {
                        reader.close();
                    } catch (IOException e) {
                        e.printStackTrace();
                    }
                }
            }

            try {
                Log.v("Network", "Buffer is "+ buffer.toString());
                JSONObject coords = new JSONObject(buffer.toString());
                t_lat  = coords.getDouble("lat");
                Log.d("Network", "Lat is "+Double.toString(t_lat));
                t_long = coords.getDouble("long");
                Log.d("Network", "Long is "+Double.toString(t_long));
            } catch (JSONException e) {
                e.printStackTrace();
            }
        }
    }
}
