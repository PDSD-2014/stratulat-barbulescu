package com.JITESH.locationwithoutgps;

import java.util.ArrayList;
import java.util.List;

import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.NameValuePair;
import org.apache.http.client.HttpClient;
import org.apache.http.client.ResponseHandler;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.impl.client.BasicResponseHandler;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.message.BasicNameValuePair;
import org.apache.http.protocol.HTTP;
import org.apache.http.protocol.HttpContext;
import org.apache.http.util.EntityUtils;

import android.app.Activity;
import android.content.Context;
import android.location.Location;
import android.location.LocationListener;
import android.location.LocationManager;
import android.os.Bundle;
import android.telephony.TelephonyManager;
import android.telephony.gsm.GsmCellLocation;
import android.util.Log;
import android.widget.TextView;
 
public class AndroidTelephonyManager extends Activity implements LocationListener {
	
   public double myLatitude, myLongitude; 
   public LocationManager mLocationManager;
   public Location location;
   public static final String whom = "CriminalLocation";
   public ResponseHandler<String> rh = new BasicResponseHandler();
   public static final String web_server_addr = "http://46.108.45.2:8080/GetAndroidData";
  
   /** Called when the activity is first created. */
   @Override
   public void onCreate(Bundle savedInstanceState) {
       super.onCreate(savedInstanceState);
       setContentView(R.layout.main);
       TextView textGsmCellLocation = (TextView)findViewById(R.id.gsmcelllocation);
       TextView textMCC = (TextView)findViewById(R.id.mcc);
       TextView textMNC = (TextView)findViewById(R.id.mnc);
       TextView textCID = (TextView)findViewById(R.id.cid);
       TextView textLAC = (TextView)findViewById(R.id.lac);
       TextView textGeo = (TextView)findViewById(R.id.geo);
       TextView textRemark = (TextView)findViewById(R.id.remark);
       
       //retrieve a reference to an instance of TelephonyManager
       TelephonyManager telephonyManager = (TelephonyManager)getSystemService(Context.TELEPHONY_SERVICE);
       GsmCellLocation cellLocation = (GsmCellLocation)telephonyManager.getCellLocation();
       
       String networkOperator = telephonyManager.getNetworkOperator();
       String mcc = networkOperator.substring(0, 3);
       String mnc = networkOperator.substring(3);
       textMCC.setText("mcc: " + mcc);
       textMNC.setText("mnc: " + mnc);
       
       int cid = cellLocation.getCid();
       int lac = cellLocation.getLac();
       textGsmCellLocation.setText(cellLocation.toString());
       textCID.setText("gsm cell id: " + String.valueOf(cid));
       textLAC.setText("gsm location area code: " + String.valueOf(lac));
       
       /* nu inteleg de ce bucata asta nu merge */
       
       mLocationManager = (LocationManager) getSystemService(Context.LOCATION_SERVICE);
       location = mLocationManager.getLastKnownLocation(LocationManager.NETWORK_PROVIDER);
       
       if(location != null) {
           // Do something with the recent location fix
           //  otherwise wait for the update below
    	   myLongitude  = location.getLongitude();
    	   myLatitude = location.getLatitude();
    	   textGeo.setText("Latitude, Longitude should be: " + String.valueOf(myLatitude) + " " + String.valueOf(myLongitude) );
    	   Log.d("LOC_FOUND", "Location setup worked, finally, hopefully no Null pointer exception");
    	   
    	   //Let's also do a HTTP POST request here, in which we inform the server
    	   //about the location and the type {criminal,victim}
    	   try {
				HttpClient client = new DefaultHttpClient();  
		        String postURL = web_server_addr;
		       
		        HttpPost post = new HttpPost(postURL); 
		 
		        List<NameValuePair> params = new ArrayList<NameValuePair>();
		 
		        params.add(new BasicNameValuePair("lat", String.valueOf(myLatitude)));
		        params.add(new BasicNameValuePair("lng", String.valueOf(myLongitude)));
		        params.add(new BasicNameValuePair("type", "CriminalLocation"));
		 
		        UrlEncodedFormEntity ent = new UrlEncodedFormEntity(params, HTTP.UTF_8);
		        post.setEntity(ent);
		 
				String responsePOST = client.execute(post, rh);  
		        String response = responsePOST;
		        Log.d("HTTP_RESPONSE", response);
			} catch (Exception e) {
				e.printStackTrace();
           }


    	   
       }
       else {
           mLocationManager.requestLocationUpdates(LocationManager.NETWORK_PROVIDER, 0, 0, this);
           Log.d("NO_LOCATION", "Location impossible to be retrieved");
       }
       
       try {
   	    Thread.sleep(1000);
	   	} catch(InterruptedException ex) {
	   	    Thread.currentThread().interrupt();
	   	}       
	}
	
	@Override
	public void onLocationChanged(Location location) {
		// TODO Auto-generated method stub
		if (location != null) {
            Log.v("Location Changed", location.getLatitude() + " and " + location.getLongitude());
        }
	}
	
	@Override
	public void onStatusChanged(String provider, int status, Bundle extras) {
		// TODO Auto-generated method stub
		
	}
	
	@Override
	public void onProviderEnabled(String provider) {
		// TODO Auto-generated method stub
		
	}
	
	@Override
	public void onProviderDisabled(String provider) {
		// TODO Auto-generated method stub
		
	}   
}
