import pymc as mc
from numpy import inf, random, empty, mean
import emcee

def sample_emcee(model=None, nwalkers=500, samples=1000, burn=500, thin=10):
    import pymc.progressbar as pbar

    # This is the likelihood function for emcee
    def lnprob(vals):
        try:
            for val,var in zip(vals,model.stochastics):
                var.value = val
            return model.logp
        except mc.ZeroProbability:
            return -1*inf

    # emcee parameters
    ndim = len(model.stochastics)

    # Find MAP
    mc.MAP(model).fit()
    start = empty(ndim)
    for i,var in enumerate(model.stochastics):
        start[i] = var.value

    # sample starting points for walkers around the MAP
    p0 = random.randn(ndim * nwalkers).reshape((nwalkers, ndim)) + start

    # instantiate sampler passing in the pymc likelihood function
    sampler = emcee.EnsembleSampler(nwalkers, ndim, lnprob)

    bar = pbar.progress_bar(burn + samples)
    i = 0

    # burn-in
    for pos, prob, state in sampler.sample(p0, iterations=burn):
        i += 1
        bar.update(i)
    sampler.reset()

    # sample
    try:
        for p, lnprob, lnlike in sampler.sample(pos, iterations=samples, 
                                                thin=thin):
            i += 1
            bar.update(i)
#    except KeyboardInterrupt:
 #       pass
    finally:
        print("\nMean acceptance fraction during sampling: {}".format(mean(sampler.acceptance_fraction)))
        mcmc = mc.MCMC(model)  # MCMC instance for model
        mcmc.sample(1, progress_bar=False) # This call is to set up the chains
        
        for i, var in enumerate(model.stochastics):
            var.trace._trace[0] = sampler.flatchain[:, i]
        
        return mcmc
        
