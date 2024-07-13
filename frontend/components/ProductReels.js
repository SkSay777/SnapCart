import React, { useState, useEffect } from 'react';
import { View, Text, Image, StyleSheet, Dimensions } from 'react-native';
import Carousel from 'react-native-snap-carousel';
import { getRecommendations } from '../api';

const { width: viewportWidth } = Dimensions.get('window');

const ProductReels = () => {
  const [products, setProducts] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const prod = 'some_product_name'; // Replace with actual product name or make it dynamic
        const nbr = 10; // Number of recommendations
        const recs = await getRecommendations(prod, nbr);
        setProducts(recs);
      } catch (err) {
        setError(err.message);
      }
    };

    fetchProducts();
  }, []);

  const renderItem = ({ item }) => (
    <View style={styles.slide}>
      <Image source={{ uri: item.ImageURL }} style={styles.image} />
      <Text style={styles.title}>{item.Name}</Text>
      <Text style={styles.brand}>Brand: {item.Brand}</Text>
      <Text style={styles.rating}>Rating: {item.Rating}</Text>
      <Text style={styles.price}>Price: ${item.Price}</Text>
    </View>
  );

  return (
    <View style={styles.container}>
      {error && <Text style={styles.error}>Error: {error}</Text>}
      <Carousel
        data={products}
        renderItem={renderItem}
        sliderWidth={viewportWidth}
        itemWidth={viewportWidth}
        layout={'stack'}
        layoutCardOffset={18}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  slide: {
    backgroundColor: 'white',
    borderRadius: 8,
    height: viewportWidth,
    padding: 50,
    justifyContent: 'center',
    alignItems: 'center',
    marginLeft: 25,
    marginRight: 25,
  },
  image: {
    width: viewportWidth - 50,
    height: viewportWidth - 50,
    borderRadius: 8,
  },
  title: {
    fontSize: 18,
    fontWeight: 'bold',
    textAlign: 'center',
    marginTop: 10,
  },
  brand: {
    fontSize: 16,
    textAlign: 'center',
    marginTop: 5,
  },
  rating: {
    fontSize: 16,
    textAlign: 'center',
    marginTop: 5,
  },
  price: {
    fontSize: 16,
    textAlign: 'center',
    marginTop: 5,
    color: 'green',
  },
  error: {
    color: 'red',
  },
});

export default ProductReels;
