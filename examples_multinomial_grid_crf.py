import numpy as np
import matplotlib.pyplot as plt

#from crf import MultinomialFixedGraphCRFNoBias
#from crf import MultinomialFixedGraphCRFNoBias
from crf import MultinomialGridCRF
#from structured_perceptron import StructuredPerceptron
import structured_svm as ssvm
import toy_datasets as ds


from IPython.core.debugger import Tracer
tracer = Tracer()


def main():
    #X, Y = generate_checker_multinomial(n_samples=10, noise=0.8)
    X, Y = ds.generate_crosses_explicit(n_samples=10, noise=10)
    #X, Y = generate_blocks_multinomial(n_samples=10, noise=0.5)
    n_labels = len(np.unique(Y))
    crf = MultinomialGridCRF(n_states=n_labels)
    #clf = StructuredPerceptron(problem=crf, max_iter=50)
    #clf = ssvm.StructuredSVM(problem=crf, max_iter=50, C=100, verbose=20,
            #check_constraints=True)
    clf = ssvm.SubgradientStructuredSVM(problem=crf, max_iter=5000, C=1,
            verbose=10, momentum=0.9, learningrate=0.05, plot=True)
    clf.fit(X, Y)
    Y_pred = np.array(clf.predict(X))
    print(clf.w)

    i = 0
    loss = 0
    for x, y, y_pred in zip(X, Y, Y_pred):
        y_pred = y_pred.reshape(x.shape[:2])
        #loss += np.sum(y != y_pred)
        loss += np.sum(np.logical_xor(y, y_pred))
        if i > 10:
            continue
        fig, plots = plt.subplots(1, 4)
        plots[0].matshow(y)
        plots[0].set_title("gt")
        w_unaries_only = np.zeros(crf.size_psi)
        w_unaries_only[:n_labels] = 1.
        unary_pred = crf.inference(x, w_unaries_only)
        plots[1].matshow(unary_pred)
        plots[1].set_title("unaries only")
        plots[2].matshow(y_pred)
        plots[2].set_title("prediction")
        loss_augmented = clf.problem.loss_augmented_inference(x, y, clf.w)
        loss_augmented = loss_augmented.reshape(y.shape)
        plots[3].matshow(loss_augmented)
        plots[3].set_title("loss augmented")
        for p in plots:
            p.set_xticks(())
            p.set_yticks(())
        fig.savefig("data_%03d.png" % i)
        #plt.close(fig)
        i += 1
    print("loss: %f" % loss)
    print("complete loss: %f" % np.sum(Y != Y_pred))

if __name__ == "__main__":
    main()
