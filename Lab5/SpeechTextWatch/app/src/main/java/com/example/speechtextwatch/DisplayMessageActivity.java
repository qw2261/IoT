package com.example.speechtextwatch;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.os.StrictMode;
import android.widget.TextView;

import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;

public class DisplayMessageActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_display_message);

        StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
        StrictMode.setThreadPolicy(policy);

        // Get the Intent that started this activity and extract the string
        Intent intent = getIntent();
        String message = intent.getStringExtra(MainActivity.EXTRA_MESSAGE);

        // Capture the layout's TextView and set the string as its text
        TextView textView = findViewById(R.id.textView);
        textView.setText(message);

        final String POST_LINK = "http://3c1bd21a.ngrok.io" + "?COMMAND=" + message;

        try {

            URL url = new URL(POST_LINK);
            HttpURLConnection client = (HttpURLConnection) url.openConnection();

            client.setRequestMethod("GET");
            int responseCode = client.getResponseCode();
            String responseBody = readResponseBody(client.getInputStream());




            System.out.println("SUCCESS");
            System.out.println(responseBody);

            TextView textView2 = findViewById(R.id.textView2);
            textView2.setText(responseBody);

        } catch (Exception e) {
            e.printStackTrace();
            System.out.println("FAIL");
        }
    }

    private String readResponseBody(InputStream inputStream) throws IOException {

        BufferedReader in = new BufferedReader(
                new InputStreamReader(inputStream));
        String inputLine;
        StringBuffer response = new StringBuffer();

        while ((inputLine = in.readLine()) != null) {
            response.append(inputLine);
        }
        in.close();

        return response.toString();
    }

}

