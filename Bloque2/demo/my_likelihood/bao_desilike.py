import os

import numpy as np
import pandas as pd
from collections import defaultdict

# function not used for now (here for when correlated bins are available)
def list_duplicates(seq):
    tally = defaultdict(list)
    for i,item in enumerate(seq):
        tally[item].append(i)
    return ((key,locs) for key,locs in tally.items() 
                            if len(locs)>1)

datasets_path = './data/'

measurements_baorsd = ['BAO_RSD/sdss_DR16_BAOplus_LRG_FSBAO_DMDHfs8.dat',
                'BAO_RSD/sdss_DR16_BAOplus_QSO_FSBAO_DMDHfs8.dat',
                'BAO_RSD/sdss_MGS_FSBAO_DVfs8.txt']
covariances_baorsd = ['BAO_RSD/sdss_DR16_BAOplus_LRG_FSBAO_DMDHfs8_covtot.txt',
               'BAO_RSD/sdss_DR16_BAOplus_QSO_FSBAO_DMDHfs8_covtot.txt',
               'BAO_RSD/sdss_MGS_FSBAO_DVfs8_covtot.txt']

measurements_bao = ['BAO/sdss_MGS_BAO_DV.txt',
                'BAO/sdss_DR12_LRG_BAO_DMDH.txt',
                'BAO/sdss_DR16_LRG_BAO_DMDH.txt',
                'BAO/sdss_DR16_QSO_BAO_DMDH.txt']
covariances_bao = ['BAO/sdss_MGS_BAO_DV_covtot.txt',
               'BAO/sdss_DR12_LRG_BAO_DMDH_covtot.txt',
               'BAO/sdss_DR16_LRG_BAO_DMDH_covtot.txt',
               'BAO/sdss_DR16_QSO_BAO_DMDH_covtot.txt']

def CompressedBAOLikelihood(cosmo=None):

    import glob
    from desilike import LikelihoodFisher
    from desilike.observables.galaxy_clustering import BAOCompressionObservable
    from desilike.likelihoods import ObservablesGaussianLikelihood
 
    if cosmo is None:
        from desilike.theories import Cosmoprimo
        cosmo = Cosmoprimo(fiducial='DESI')
        cosmo.params = {'Omega_m': {'prior': {'limits': [0.1, 0.9]}, 'ref': {'dist': 'norm', 'loc': 0.3, 'scale': 0.002}, 'latex': '\Omega_m'},
                        'omega_b': {'prior': {'dist': 'norm', 'loc': 0.02236, 'scale': 0.0005}, 'latex': '\omega_b'},
                        'H0':  {'prior': {'limits': [20., 100.]}, 'ref': {'dist': 'norm', 'loc': 70., 'scale': 1.}, 'latex': 'H_{0}'}}

    likelihood = 0
    # New lines
    for i in range(len(measurements_bao)):
        # Load datavector and effective redshift
        df = pd.read_csv(datasets_path + measurements_bao[i], delim_whitespace=True, names=["redshift", "mean", "label"])
        # get array for effective redshifts
        if len(df["redshift"])==1:
            redshifts = [(df["redshift"],[0])]
        else:
            redshifts = sorted(list_duplicates(df["redshift"]))
        # define lists of observables
        observables = []
        for j in range(len(redshifts)):
            datavector = df["mean"][redshifts[j][1]].tolist()
            labels = df["label"][redshifts[j][1]].tolist()
            labels = [label.replace('rs', 'rd') for label in labels]
            observable = BAOCompressionObservable(cosmo=cosmo, data=datavector, quantities=labels, z=redshifts[j][0])
            observables.append(observable)
        # Load covariance matrix
        cov = np.loadtxt(datasets_path + covariances_bao[i])
        # append likelihood
        likelihood = likelihood + ObservablesGaussianLikelihood(observables=observables, covariance=cov)
    likelihood.params['desi_bao.loglikelihood'] = likelihood.params['desi_bao.logprior'] = {}
    #likelihood = CompressedBAORSDLikelihood()
    #print(likelihood())
    return likelihood

def CompressedBAORSDLikelihood(cosmo=None):

    import glob
    
    import numpy as np
    import pandas as pd
    from desilike import LikelihoodFisher
    from desilike.observables.galaxy_clustering import BAOCompressionObservable, StandardCompressionObservable
    from desilike.likelihoods import ObservablesGaussianLikelihood

    convert = {'f_sigma8': 'fsigmar'}
 
    if cosmo is None:
        from desilike.theories import Cosmoprimo
        cosmo = Cosmoprimo(fiducial='DESI')
        cosmo.params = {'Omega_m': {'prior': {'limits': [0.1, 0.9]}, 'ref': {'dist': 'norm', 'loc': 0.3, 'scale': 0.002}, 'latex': '\Omega_m'},
                        'omega_b': {'prior': {'dist': 'norm', 'loc': 0.02236, 'scale': 0.0005}, 'latex': '\omega_b'},
                        'H0':  {'prior': {'limits': [20., 100.]}, 'ref': {'dist': 'norm', 'loc': 70., 'scale': 1.}, 'latex': 'H_{0}'}}

    likelihood = 0
    # New lines
    for i in range(len(measurements_baorsd)):
        # Load datavector and effective redshift
        df = pd.read_csv(datasets_path + measurements_baorsd[i], delim_whitespace=True, names=["redshift", "mean", "label"])
        # get array for effective redshifts
        redshifts = sorted(list_duplicates(df["redshift"]))
        # define lists of observables
        observables = []
        for j in range(len(redshifts)):
            datavector = df["mean"][redshifts[j][1]].tolist()
            labels = df["label"][redshifts[j][1]].tolist()
            labels = [convert.get(label, label).replace('rs', 'rd') for label in labels]
            observable = StandardCompressionObservable(cosmo=cosmo, data=datavector, quantities=labels, z=redshifts[j][0], r=8.)
            observables.append(observable)
        # Load covariance matrix
        cov = np.loadtxt(datasets_path + covariances_baorsd[i])
        # append likelihood
        likelihood = likelihood + ObservablesGaussianLikelihood(observables=observables, covariance=cov)
    likelihood.params['desi_bao.loglikelihood'] = likelihood.params['desi_bao.logprior'] = {}
    #likelihood = CompressedBAORSDLikelihood()
    #print(likelihood())
    return likelihood


if __name__ == '__main__':

    import argparse
    parser = argparse.ArgumentParser(description='Y1 cosmological forecasts')
    parser.add_argument('--todo', type=str, nargs='*', required=False, default=[], choices=['forecasts', 'tests', 'bindings', 'sampling'])
    args = parser.parse_args()

    from desilike import setup_logging
    from desilike.bindings import CobayaLikelihoodGenerator, CosmoSISLikelihoodGenerator, MontePythonLikelihoodGenerator

    chains_dir = 'desilike'
    Likelihoods = [CompressedBAOLikelihood, CompressedBAORSDLikelihood]
    
    if 'tests' in args.todo:
        setup_logging('info')
        for Likelihood in Likelihoods:
            print(Likelihood()())  # non-zero likelihood comes from omega_b prior

    if 'bindings' in args.todo:
        setup_logging('info')
        kw_like = {'cosmo': 'external'}
        CobayaLikelihoodGenerator()(Likelihoods, kw_like=kw_like)
        CosmoSISLikelihoodGenerator()(Likelihoods, kw_like=kw_like)
        MontePythonLikelihoodGenerator()(Likelihoods, kw_like=kw_like)

    if 'sampling' in args.todo:
        setup_logging('info')
        likelihood_names = ['bao']

        from desilike.theories import Cosmoprimo
        from desilike.samplers import ZeusSampler, EmceeSampler

        cosmo = Cosmoprimo(fiducial='DESI')
        cosmo.params = {'Omega_m': {'prior': {'limits': [0.1, 0.9]}, 'ref': {'dist': 'norm', 'loc': 0.3, 'scale': 0.002}, 'latex': '\Omega_m'},
                        'omega_b': {'prior': {'dist': 'norm', 'loc': 0.02236, 'scale': 0.0005}, 'latex': '\omega_b'},
                        'H0':  {'prior': {'limits': [20., 100.]}, 'ref': {'dist': 'norm', 'loc': 70., 'scale': 1.}, 'latex': 'H_{0}'}}
        likelihoods = []
        
        if 'bao_rsd' in likelihood_names:
            likelihood = CompressedBAORSDLikelihood(cosmo=cosmo)
            likelihoods.append(likelihood)

        elif 'bao' in likelihood_names:
            likelihood = CompressedBAOLikelihood(cosmo=cosmo)
            likelihoods.append(likelihood)

        sampler = EmceeSampler(sum(likelihoods), chains=1, nwalkers=20, seed=42, save_fn=os.path.join(chains_dir, '_chains_{}'.format('_'.join(likelihood_names)), 'chain.*.npy'))
        sampler.run(check={'max_eigen_gr': 0.02})
