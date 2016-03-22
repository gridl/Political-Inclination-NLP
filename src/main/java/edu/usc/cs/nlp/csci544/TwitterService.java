/*
 * Licensed to the Apache Software Foundation (ASF) under one or more
 * contributor license agreements.  See the NOTICE file distributed with
 * this work for additional information regarding copyright ownership.
 * The ASF licenses this file to You under the Apache License, Version 2.0
 * (the "License"); you may not use this file except in compliance with
 * the License.  You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package edu.usc.cs.nlp.csci544;

import java.util.List;

import twitter4j.Query;
import twitter4j.QueryResult;
import twitter4j.Status;
import twitter4j.Twitter;
import twitter4j.TwitterException;
import twitter4j.TwitterFactory;
import twitter4j.auth.AccessToken;

public class TwitterService {

	private Twitter twitter;
	private String consumerKey = "BlweSNHSKmeSur5YkXMxzkUUV";
	private String consumerKeySecret = "KocCMLcrY4u34eqt2UNSm9wk89MZdrRSjKfZdzJxVgKNT56aCI";
	private String tokenKey = "4317032720-yxQUoRRj6SZtDSSf7RsgvSCjukEHFNbQGbWJPpY";
	private String tokenKeySecret = "UWRd46OzsWezffVASlQpzgJ8EMUcX2HHZPFadw4bM7K9k";
	
	/**
	 * Initialize Twitter Service
	 */
	public TwitterService() {
		twitter = TwitterFactory.getSingleton();
		twitter.setOAuthConsumer(consumerKey, consumerKeySecret);
		AccessToken token = new AccessToken(tokenKey, tokenKeySecret);
		twitter.setOAuthAccessToken(token);
	}
	
	/**
	 * Retrieve Tweets from User's Timeline
	 * @return
	 * @throws TwitterException
	 */
	public List<Status> getTimelineTweets() throws TwitterException {
		return twitter.getHomeTimeline();
	}
	
	/**
	 * Search Tweets based on HashTag
	 * @param hashtag
	 * @return
	 * @throws TwitterException
	 */
	public List<Status> searchTweets(String hashtag) throws TwitterException {
		Query query = new Query(hashtag);
		
		// Number of Tweets
		query.setCount(100);
		// Set Language
		query.setLang("es");
		
		QueryResult result = twitter.search(query);
		return result.getTweets();
	}
	
	/*
	 * Print Tweets
	 */
	public void printTweets(List<Status> tweets) {
		for(Status status: tweets) {
			System.out.println(status.getUser().getName() + ": " + status.getText());
		}
	}
	
	/**
	 * Test the Service
	 * @param args
	 * @throws TwitterException
	 */
	public static void main(String[] args) throws TwitterException {
		TwitterService service = new TwitterService();
		service.printTweets(service.searchTweets("#GOPDebate"));
	}
}
