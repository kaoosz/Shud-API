<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Http\Resources\CandidateResource;
use App\Http\Resources\VotesCitiesResouce2014;
use App\Models\Candidate;
use App\Models\VotesCities_2012;
use App\Models\VotesCities_2014;
use App\Models\VotesCities_2016;
use App\Models\VotesCities_2018;
use App\Models\VotesCities_2020;
use App\Models\Votesneighborhood;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;

class CandidateResourceController extends Controller
{
    /**
     * Display a listing of the resource.
     *
     * @return \Illuminate\Http\Response
     */

    public function dados($qt)
    {

        if(request()->get('top_bairro') == 'bairro2020' and request()->get('UF')){

            $can = Votesneighborhood::query()
            ->select('NM_VOTAVEL','NR_VOTAVEL','DT_GERACAO_HH_GERACAO','DS_CARGO_PERGUNTA','NM_MUNICIPIO','NM_BAIRRO','QT_VOTOS')
            ->orderByDesc('QT_VOTOS')
            ->whereNotIn('NM_VOTAVEL',['NULO','BRANCO'])
            ->where('NM_MUNICIPIO',request()->get('UF'))
            ->get();

            $uniq = $can->uniqueStrict('NM_VOTAVEL')->take($qt); // isso usa 170 kb
            //return VotesCitiesResouce2014::collection($uniq);
            return $uniq;

        }else if(request()->get('top_bairro') == 'bairro2020'){
            $can = Votesneighborhood::query()
            ->select('NM_VOTAVEL','NR_VOTAVEL','DT_GERACAO_HH_GERACAO','DS_CARGO_PERGUNTA','NM_MUNICIPIO','NM_BAIRRO','QT_VOTOS')
            ->orderByDesc('QT_VOTOS')
            ->whereNotIn('NM_VOTAVEL',['NULO','BRANCO'])
            ->take(4000)
            ->get();

            $uniq = $can->uniqueStrict('NM_VOTAVEL')->take($qt); // isso usa 170 kb
            //return VotesCitiesResouce2014::collection($uniq);
            return $uniq;

        }

        dd('NAO PASSAR');
        dd('NAO PASSAR');
        dd('NAO PASSAR');

        if(request()->get('top_bairro') == 'bairro2020' and request()->get('UF')){

            $can = Votesneighborhood::query()
            ->select('NM_VOTAVEL','NR_VOTAVEL','DT_GERACAO_HH_GERACAO','DS_CARGO_PERGUNTA','NM_MUNICIPIO','NM_BAIRRO','QT_VOTOS')
            ->orderByDesc('QT_VOTOS')
            ->whereNotIn('NM_VOTAVEL',['NULO','BRANCO'])
            ->where('NM_MUNICIPIO',request()->get('UF'))
            ->get();

            $uniq = $can->uniqueStrict('NM_VOTAVEL')->take($qt); // isso usa 170 kb
            return VotesCitiesResouce2014::collection($uniq);

        }else if(request()->get('top_bairro') == 'bairro2020'){
            $can = Votesneighborhood::query()
            ->select('NM_VOTAVEL','NR_VOTAVEL','DT_GERACAO_HH_GERACAO','DS_CARGO_PERGUNTA','NM_MUNICIPIO','NM_BAIRRO','QT_VOTOS')
            ->orderByDesc('QT_VOTOS')
            ->whereNotIn('NM_VOTAVEL',['NULO','BRANCO'])
            ->take(4000)
            ->get();
            $uniq = $can->uniqueStrict('NM_VOTAVEL')->take($qt); // isso usa 170 kb
            return VotesCitiesResouce2014::collection($uniq);
           // return $uniq;
        }


        // 'bairro2020' => $this->when($request->get('bairro') === 'bairro2020',function() use($request){
        //     if($request->get('UF') and $request->get('bairro') === 'bairro2020'){
        //         return $this->bairro2020()->where("NM_MUNICIPIO", request()->get('UF'))->paginate(10);
        //     }
        //     return $this->bairro2020()->where("NR_VOTAVEL", request()->get('NR_CANDIDATO'))->paginate(10);
        // }),


        if(request()->get('ANO') == 2020 && request()->get('top_cidade') == 'cidade2020'){
            $can = VotesCities_2020::query()
            ->select("NM_VOTAVEL","NR_VOTAVEL","DT_GERACAO_HH_GERACAO","DS_CARGO_PERGUNTA","NM_MUNICIPIO","QT_VOTOS")
            ->whereNotIn('NM_VOTAVEL',['NULO','BRANCO'])
            ->orderByDesc('QT_VOTOS')
            ->take(1000)
            ->get();

            $arm = $can->uniqueStrict('NM_VOTAVEL')->take($qt);

            return $arm;
            //return VotesCitiesResouce2014::collection($can);

        }else if(request()->get('ANO') == 2018 && request()->get('top_cidade') == 'cidade2018'){
            $can = VotesCities_2018::query()
            ->select("NM_VOTAVEL","NR_VOTAVEL","DT_GERACAO_HH_GERACAO","DS_CARGO_PERGUNTA","NM_MUNICIPIO","QT_VOTOS")
            ->whereNotIn('NM_VOTAVEL',['NULO','BRANCO'])
            ->orderByDesc('QT_VOTOS')
            ->take(1000)
            ->get();
            $arm = $can->uniqueStrict('NM_VOTAVEL')->take($qt);

            return $arm;

        }else if(request()->get('ANO') == 2016 && request()->get('top_cidade') == 'cidade2016'){
            $can = VotesCities_2016::query()
            ->select("NM_VOTAVEL","NR_VOTAVEL","DT_GERACAO_HH_GERACAO","DS_CARGO_PERGUNTA","NM_MUNICIPIO","QT_VOTOS")
            ->whereNotIn('NM_VOTAVEL',['NULO','BRANCO'])
            ->orderByDesc('QT_VOTOS')
            ->take(1000)
            ->get();
            $arm = $can->uniqueStrict('NM_VOTAVEL')->take($qt);

            return $arm;

        }else if(request()->get('ANO') == 2014 && request()->get('top_cidade') == 'cidade2014'){
            $can = VotesCities_2014::query()
            ->select("NM_VOTAVEL","NR_VOTAVEL","DT_GERACAO_HH_GERACAO","DS_CARGO_PERGUNTA","NM_MUNICIPIO","QT_VOTOS")
            ->whereNotIn('NM_VOTAVEL',['NULO','BRANCO'])
            ->orderByDesc('QT_VOTOS')
            ->take(1000)
            ->get();
            $arm = $can->uniqueStrict('NM_VOTAVEL')->take($qt);

            return $arm;

        }else if(request()->get('ANO') == 2012 && request()->get('top_cidade') == 'cidade2012'){
            $can = VotesCities_2012::query()
            ->select("NM_VOTAVEL","NR_VOTAVEL","DT_GERACAO_HH_GERACAO","DS_CARGO_PERGUNTA","NM_MUNICIPIO","QT_VOTOS")
            ->whereNotIn('NM_VOTAVEL',['NULO','BRANCO'])
            ->orderByDesc('QT_VOTOS')
            ->take(1000)
            ->get();
            $arm = $can->uniqueStrict('NM_VOTAVEL')->take($qt);

            return $arm;

        }
        else{
            return 'else';
        }


        // contem nulos e repetidos

        //return VotesCitiesResouce2014::collection($vv);
    }
    public function index(Candidate $candidate)
    {

        $can = Candidate::query()->paginate(10);//->when(request()->get('show') === 'bairro2018',
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

        if(!request()->get('ANO') or !request()->get('NR_CANDIDATO') ){
            $can = Candidate::query()
            ->where('NM_URNA_CANDIDATO',request()->get('urna'))->paginate(10);
        }

        if(request()->get('ANO')){
            $can = Candidate::query()
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

            ->when(request()->get('bairro') === 'bairro2020',fn($query) => $query->with('bairro2020'))
            ->when(request()->get('bairro') === 'bairro2018',fn($query) => $query->with('bairro2018'))
            ->when(request()->get('bairro') === 'bairro2016',fn($query) => $query->with('bairro2016'))
            ->when(request()->get('bairro') === 'bairro2014',fn($query) => $query->with('bairro2014'))
            ->when(request()->get('bairro') === 'bairro2012',fn($query) => $query->with('bairro2012'))

            ->where([['NM_URNA_CANDIDATO',request()->get('urna')],
            ['ANO_ELEICAO',request()->get('ANO')],
            ['NR_CANDIDATO',request()->get('NR_CANDIDATO')]]
        )->get();
        }

        // $fun = $request->only(['ANO','NR_CANDIDATO']);

        // dd($fun);

        return CandidateResource::collection($can);

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
