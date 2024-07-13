import React from 'react';
import { SafeAreaView, StyleSheet } from 'react-native';
import ProductReels from './components/ProductReels';

const App = () => {
  return (
    <SafeAreaView style={styles.container}>
      <ProductReels />
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
});

export default App;
