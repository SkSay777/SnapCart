import React, { useState } from 'react';
import { View, Text, Button, FlatList, Image } from 'react-native';
import { getRecommendations } from '../api';

const Recommendations = () => {
  const [recommendations, setRecommendations] = useState([]);
  const [error, setError] = useState(null);

  const fetchRecommendations = async () => {
    try {
      const prod = 'some_product_name'; // Replace with actual product name
      const nbr = 10; // Number of recommendations
      const recs = await getRecommendations(prod, nbr);
      setRecommendations(recs);
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <View>
      <Button title="Get Recommendations" onPress={fetchRecommendations} />
      {error && <Text>Error: {error}</Text>}
      <FlatList
        data={recommendations}
        keyExtractor={(item, index) => index.toString()}
        renderItem={({ item }) => (
          <View>
            <Image source={{ uri: item.ImageURL }} style={{ width: 100, height: 100 }} />
            <Text>{item.Name}</Text>
            <Text>Brand: {item.Brand}</Text>
            <Text>Rating: {item.Rating}</Text>
            <Text>Price: ${item.Price}</Text>
          </View>
        )}
      />
    </View>
  );
};

export default Recommendations;
