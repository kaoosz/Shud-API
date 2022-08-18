<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Http\Resources\CandidateResource;
use App\Models\Candidate;
use Illuminate\Http\Request;

class CandidateResourceController extends Controller
{
    /**
     * Display a listing of the resource.
     *
     * @return \Illuminate\Http\Response
     */
    private $candidate;

    public function __construct(Candidate $candidate)
    {
        $this->candidate = $candidate;
    }

    public function index(Candidate $candidate)
    {

        $can = Candidate::query()->paginate();//->when(request()->get('show') === 'bairro2018',
        //fn($query) => $query->with('bairro2018'))->paginate(3);

        return CandidateResource::collection($can);

    }

    /**
     * Store a newly created resource in storage.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\Response
     */
    public function store(Request $request)
    {
        //
    }

    /**
     * Display the specified resource.
     *
     * @param  \App\Models\Candidate  $candidate
     * @return \Illuminate\Http\Response
     */
    public function show(Candidate $candidate,Request $request)
    {

        $can = Candidate::query()
        ->where('NM_URNA_CANDIDATO',request()->get('urna'))->paginate();//->get();


        if(request()->get('ANO')){
            $can = Candidate::query()
            //  ->with(['votesneighborhood','bairro2018','bairro2016','bairro2014','bairro2012',
            //  'schools2020','schools2018','schools2016','schools2014','schools2012',
            //  'cities2020','cities2018','cities2016','cities2014','cities2012'])
            ->when(request()->get('escola') === 'schools2020',fn($query) => $query->with('schools2020'))
            ->when(request()->get('escola') === 'schools2018',fn($query) => $query->with('schools2018'))
            ->when(request()->get('escola') === 'schools2016',fn($query) => $query->with('schools2016'))
            ->when(request()->get('escola') === 'schools2014',fn($query) => $query->with('schools2014'))
            ->when(request()->get('escola') === 'schools2012',fn($query) => $query->with('schools2012'))

            ->when(request()->get('cidade') === 'cities2020',fn($query) => $query->with('cities2020'))
            ->when(request()->get('cidade') === 'cities2018',fn($query) => $query->with('cities2018'))
            ->when(request()->get('cidade') === 'cities2016',fn($query) => $query->with('cities2016'))
            ->when(request()->get('cidade') === 'cities2014',fn($query) => $query->with('cities2014'))
            ->when(request()->get('cidade') === 'cities2012',fn($query) => $query->with('cities2012'))

            ->when(request()->get('bairro') === 'votesneighborhood',fn($query) => $query->with('votesneighborhood'))
            ->when(request()->get('bairro') === 'bairro2018',fn($query) => $query->with('bairro2018'))
            ->when(request()->get('bairro') === 'bairro2016',fn($query) => $query->with('bairro2016'))
            ->when(request()->get('bairro') === 'bairro2014',fn($query) => $query->with('bairro2014'))
            ->when(request()->get('bairro') === 'bairro2012',fn($query) => $query->with('bairro2012'))

            ->where([['NM_URNA_CANDIDATO',request()->get('urna')],
            ['ANO_ELEICAO',request()->get('ANO')],
            ['NR_CANDIDATO',request()->get('NR_CANDIDATO')]]
            )->paginate();//->get();//->get();
        }

        return CandidateResource::collection($can);

        // $can = Candidate::query()->when(request()->get('bairro') === 'votesneighborhood',//'votesneighborhood',
        // fn($query) => $query->with('votesneighborhood'))
        // ->where('NM_URNA_CANDIDATO',"{$nome}")
        // ->get();
    }

    /**
     * Update the specified resource in storage.
     *
     * @param  \Illuminate\Http\Request  $request
     * @param  \App\Models\Candidate  $candidate
     * @return \Illuminate\Http\Response
     */
    public function update(Request $request, Candidate $candidate)
    {
        //
    }

    /**
     * Remove the specified resource from storage.
     *
     * @param  \App\Models\Candidate  $candidate
     * @return \Illuminate\Http\Response
     */
    public function destroy(Candidate $candidate)
    {
        //
    }
}
