
# Load libraries
import numpy as np
import pylab as pl
from sklearn import datasets
from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import NearestNeighbors
from sklearn import metrics, grid_search
from sklearn.cross_validation import train_test_split
from sklearn.metrics import make_scorer


def load_data():
    '''Load the Boston dataset.'''
    boston = datasets.load_boston()
    return boston


def explore_city_data(city_data):
    '''Calculate the Boston housing statistics.'''
    # Get the labels and features from the housing data
    housing_prices = city_data.target
    print housing_prices
    housing_features = city_data.data
    print housing_features

    sizeData = len(housing_prices)
    print("sizeData:" + str(sizeData))
    sizeFeatures = housing_features.shape[1]
    print("sizeFeature:" + str(sizeFeatures))
    minVal = np.min(housing_prices)
    print("minVal:" + str(minVal))
    maxVal = np.max(housing_prices)
    print("maxVal:" + str(maxVal))
    mean = np.mean(housing_prices)
    print("mean:" + str(mean))
    median = np.median(housing_prices)
    print("median:" + str(median))
    sdeviation = np.std(housing_prices)
    print("sdeviation:" + str(sdeviation))


def performance_metric(label, prediction):
    # Calculate and return the appropriate performance metric
    metric = metrics.mean_squared_error(label, prediction)
    return metric


def split_data(city_data):
    # Get the features and labels from the Boston housing data
    X, y = city_data.data, city_data.target

    # Randomly shuffle the sample set. Divide it into training and testing set.
    X_train, X_test, y_train, y_test= train_test_split(X,y, test_size=0.30, random_state=42)

    return X_train, y_train, X_test, y_test


def learning_curve(depth, X_train, y_train, X_test, y_test):
    # Calculate the performance of the model after a set of training data.

    # We will vary the training set size so that we have 50 different sizes
    sizes = np.linspace(1, len(X_train), 50)
    train_err = np.zeros(len(sizes))
    test_err = np.zeros(len(sizes))

    print "Decision Tree with Max Depth: "
    print depth

    for i, s in enumerate(sizes):
        # Create and fit the decision tree regressor model
        regressor = DecisionTreeRegressor(max_depth=depth)
        regressor.fit(X_train[:s], y_train[:s])

        # Find the performance on the training and testing set
        train_err[i] = performance_metric(y_train[:s], regressor.predict(X_train[:s]))
        test_err[i] = performance_metric(y_test, regressor.predict(X_test))


    # Plot learning curve graph
    learning_curve_graph(sizes, train_err, test_err)


def learning_curve_graph(sizes, train_err, test_err):
    '''Plot training and test error as a function of the training size.'''
    pl.figure()
    pl.title('Decision Trees: Performance vs Training Size')
    pl.plot(sizes, test_err, lw=2, label='test error')
    pl.plot(sizes, train_err, lw=2, label='training error')
    pl.legend()
    pl.xlabel('Training Size')
    pl.ylabel('Error')
    pl.show()


def model_complexity(X_train, y_train, X_test, y_test):
    '''Calculate the performance of the model as model complexity increases.'''

    print "Model Complexity: "

    # We will vary the depth of decision trees from 2 to 25
    max_depth = np.arange(1, 25)
    train_err = np.zeros(len(max_depth))
    test_err = np.zeros(len(max_depth))

    for i, d in enumerate(max_depth):
        # Setup a Decision Tree Regressor so that it learns a tree with depth d
        regressor = DecisionTreeRegressor(max_depth=d)

        # Fit the learner to the training data
        regressor.fit(X_train, y_train)

        # Find the performance on the training set
        train_err[i] = performance_metric(y_train, regressor.predict(X_train))

        # Find the performance on the testing set
        test_err[i] = performance_metric(y_test, regressor.predict(X_test))

    # Plot the model complexity graph
    model_complexity_graph(max_depth, train_err, test_err)


def model_complexity_graph(max_depth, train_err, test_err):
    '''Plot training and test error as a function of the depth of the decision tree learn.'''

    pl.figure()
    pl.title('Decision Trees: Performance vs Max Depth')
    pl.plot(max_depth, test_err, lw=2, label='test error')
    pl.plot(max_depth, train_err, lw=2, label='training error')
    pl.legend()
    pl.xlabel('Max Depth')
    pl.ylabel('Error')
    pl.show()


def fit_predict_model(city_data):
    '''Find and tune the optimal model. Make a prediction on housing data.'''

    # Get the features and labels from the Boston housing data
    X, y = city_data.data, city_data.target

    # Setup a Decision Tree Regressor
    regressor = DecisionTreeRegressor()

    parameters = {'max_depth': (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)}

    # find the best performance metric
    scoring = make_scorer(metrics.mean_squared_error, False)

    # gridearch to fine tune the Decision Tree Regressor and find the best model
    reg = grid_search.GridSearchCV(regressor, parameters, scoring)

    # Fit the learner to the training data
    print "Final Model: "

    print reg.fit(X, y)
    print "Best model parameter:  " + str(reg.best_params_)
    print "Best estimator:  " + str(reg.best_estimator_)

    est = reg.best_estimator_   # Retrieve the best estimator found by GridSearchCV.

    # Use the model to predict the output of a particular sample
    x = [11.95, 0.00, 18.100, 0, 0.6590, 5.6090, 90.00, 1.385, 24, 680.0, 20.20, 332.09, 12.13]
    y = reg.predict(x)
    print "House: " + str(x)
    print "Prediction: " + str(y)
    y = est.predict(x)          # Use the object est to make a prediction.
    print "Best Prediction:  " + str(y)

    # Identifies if the prediction is reasonable by finding the nearest neighbor by the feature vector
    indexes = find_nearest_neighbor_indexes(x, X)
    sum_prices = []
    for i in indexes:
        sum_prices.append(city_data.target[i])
    neighbor_avg = np.mean(sum_prices)
    print "Nearest Neighbors average: " +str(neighbor_avg)

def find_nearest_neighbor_indexes(x, X):
    # find the nearest neighbor by based on the features
    neigh = NearestNeighbors( n_neighbors = 10 )
    neigh.fit( X)
    distance, indexes = neigh.kneighbors( x )
    return indexes

def main():
    '''Analyze the Boston housing data. Evaluate and validate the
    performanance of a Decision Tree regressor on the Boston data.
    Fine tune the model to make prediction on unseen data.'''

    # Load data
    city_data = load_data()

    # Explore the data
    explore_city_data(city_data)

    # Training/Test dataset split
    X_train, y_train, X_test, y_test = split_data(city_data)

    # Learning Curve Graphs
    max_depths = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    for max_depth in max_depths:
        learning_curve(max_depth, X_train, y_train, X_test, y_test)

    # Model Complexity Graph
    model_complexity(X_train, y_train, X_test, y_test)

    # Tune and predict Model
    fit_predict_model(city_data)


main()