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
	
//Configuration variables: 
   public static final String whom = "CriminalLocation";
   public static final String web_server_addr = "http://46.108.45.2:8080/GetAndroidData";
   public static final String location_provider = LocationManager.NETWORK_PROVIDER;
   
   	//variables to be called in requestLocationUpdates()
   public static final int delay_ms_loc = 400;
   public static final int min_dist = 1; //in meters
   
   	//if true, assumes that we are running app on a mobile phone with sim, to get
    //extra info from GSM
   public boolean use_sim = false;

   public double myLatitude, myLongitude; 
   public LocationManager mLocationManager;
   public Location location;
   
   public ResponseHandler<String> rh = new BasicResponseHandler();
   
   public TextView textGeo; 
   public TextView textRemark;
   public TextView logDebug;
   
   public int loc_chg_cnt = 0;
  
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
       textGeo = (TextView)findViewById(R.id.geo);
       textRemark = (TextView)findViewById(R.id.remark);
       logDebug = (TextView)findViewById(R.id.debug_msg);
       
       //retrieve a reference to an instance of TelephonyManager
       if(use_sim) {
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
       }
     
       mLocationManager = (LocationManager) getSystemService(Context.LOCATION_SERVICE);
       location = mLocationManager.getLastKnownLocation(location_provider);
       
       if(location != null) {
           // Do something with the recent location fix
           //  otherwise wait for the update below
    	   myLongitude  = location.getLongitude();
    	   myLatitude = location.getLatitude();
    	   textGeo.setText("Latitude, Longitude should be: " + String.valueOf(myLatitude) + " " + String.valueOf(myLongitude) );
    	   Log.d("LOC_FOUND", "Location setup worked, finally, hopefully no Null pointer exception");
    	   textRemark.setText("LOC_FOUND - Location setup done, trying HTTP request to server ...");
    	   logDebug.setText("LOC_FOUND - Location setup done, now trying HTTP request to server ...");
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
		        textRemark.setText("HTTP POST Request succesfully sent. Our response is: " + response);
		        loc_chg_cnt++;
		    	logDebug.setText("HTTP_DEBUG - Received HTTP response from server. Counter = " + String.valueOf(loc_chg_cnt));

			} catch (Exception e) {
				e.printStackTrace(); 
           }
       }
       else {
    	   
           mLocationManager.requestLocationUpdates(LocationManager.NETWORK_PROVIDER, delay_ms_loc, min_dist, this);
           Log.d("NO_LOCATION" , "Location impossible to be retrieved");
     	   textRemark.setText("NO_LOCATION - Location impossible to be retrieved ...");
       }
              
	}
   
   @Override
   protected void onResume() {
	  super.onResume();
	  mLocationManager.requestLocationUpdates(location_provider, delay_ms_loc, min_dist, this);
	  Log.v("NEW_LOCATION?", "Resuming app, requestLocationUpdates was called");
	  //textRemark.setText("NEW_LOCATION? Resuming app, requestLocationUpdates() was called");
	  logDebug.setText("NEW_LOCATION? Resuming app, requestLocationUpdates() was called");
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
	        Log.d("HTTP_RESPONSE_RESUME", response);
	        textRemark.setText("HTTP POST RESUME Request succesfully sent. Our response is: " + response);
	        loc_chg_cnt++;
	        logDebug.setText("Sent HTTP request from requestLocationUpdates() function Counter = " + String.valueOf(loc_chg_cnt)); 
		} catch (Exception e) {
			e.printStackTrace(); 
        }

	}
	
	@Override
	public void onLocationChanged(Location location) {
		if (location != null) {
            Log.v("Location Changed", location.getLatitude() + " and " + location.getLongitude());
     	    myLongitude  = location.getLongitude();
     	    myLatitude = location.getLatitude();
     	    textGeo.setText("Latitude, Longitude should be: " + String.valueOf(myLatitude) + " " + String.valueOf(myLongitude) );
	        //logDebug.setText("Sent HTTP request from requestLocationUpdates() function"); 
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
     		        Log.d("HTTP_RESPONSE_LOC_CHG", response);
     		        textRemark.setText("HTTP POST LOCATION CHANGED Request succesfully sent. Our response is: " + response);
     		        loc_chg_cnt++;
     		        logDebug.setText("Sent HTTP request from onLocationChanged() function. Counter = " + String.valueOf(loc_chg_cnt)); 
     			} catch (Exception e) {
     				e.printStackTrace(); 
     	        }


        } else {
            Log.v("NO_NEW_LOCATION", "No new location in onLocationChanged()");
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
