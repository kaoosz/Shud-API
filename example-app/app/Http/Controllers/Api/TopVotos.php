<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Http\Resources\VotesCities_2020 as ResourcesVotesCities_2020;
use App\Http\Resources\VotesCitiesResouce2014;
use App\Http\Resources\VotesCitiesResource2012;
use App\Http\Resources\VotesCitiesResource2016;
use App\Http\Resources\VotesCitiesResource2018;
use App\Http\Resources\VotesCitiesResource2020;
use App\Models\VotesCities_2020;
use App\Models\VotesCities_2018;
use App\Models\VotesCities_2016;
use App\Models\VotesCities_2014;
use App\Models\VotesCities_2012;
use Illuminate\Http\Request;

class TopVotos extends Controller
{


    public function CidadeMaisVotada($qt)
    {
        if(request()->get('ANO') == 2020 and request()->get('top_cidade') == 'cidade2020' and
        request()->get('MUNICIPIO')){
            $can = VotesCities_2020::query()
            ->whereNotIn('NM_VOTAVEL',['NULO','BRANCO'])
            ->where('NM_MUNICIPIO',request()->get('MUNICIPIO'))
            ->orderByDesc('QT_VOTOS')
            ->take(5000)
            ->get();

            $arm = $can->uniqueStrict('NM_VOTAVEL')->take($qt);
            return VotesCitiesResource2020::collection($arm);

        }else if(request()->get('ANO') == 2020 && request()->get('top_cidade') == 'cidade2020'){
            $can = VotesCities_2020::query()
            ->whereNotIn('NM_VOTAVEL',['NULO','BRANCO'])
            ->orderByDesc('QT_VOTOS')
            ->take(5000)
            ->get();

            $arm = $can->uniqueStrict('NM_VOTAVEL')->take($qt);
            return VotesCitiesResource2020::collection($arm);

        }else if(request()->get('ANO') == 2018 && request()->get('top_cidade') == 'cidade2018' and
        request()->get('MUNICIPIO')){
            $can = VotesCities_2018::query()
            ->whereNotIn('NM_VOTAVEL',['NULO','BRANCO'])
            ->where('NM_MUNICIPIO',request()->get('MUNICIPIO'))
            ->orderByDesc('QT_VOTOS')
            ->take(5000)
            ->get();

            $arm = $can->uniqueStrict('NM_VOTAVEL')->take($qt);
            return VotesCitiesResource2018::collection($arm);

        }else if(request()->get('ANO') == 2018 && request()->get('top_cidade') == 'cidade2018'){
            $can = VotesCities_2018::query()
            ->whereNotIn('NM_VOTAVEL',['NULO','BRANCO'])
            ->orderByDesc('QT_VOTOS')
            ->take(5000)
            ->get();

            $arm = $can->uniqueStrict('NM_VOTAVEL')->take($qt);
            return VotesCitiesResource2018::collection($arm);

        }else if(request()->get('ANO') == 2016 && request()->get('top_cidade') == 'cidade2016' and
        request()->get('MUNICIPIO')){
            $can = VotesCities_2016::query()
            ->whereNotIn('NM_VOTAVEL',['NULO','BRANCO'])
            ->where('NM_MUNICIPIO',request()->get('MUNICIPIO'))
            ->orderByDesc('QT_VOTOS')
            ->take(5000)
            ->get();

            $arm = $can->uniqueStrict('NM_VOTAVEL')->take($qt);
            return VotesCitiesResource2016::collection($arm);

        }else if(request()->get('ANO') == 2016 && request()->get('top_cidade') == 'cidade2016'){
            $can = VotesCities_2016::query()
            ->whereNotIn('NM_VOTAVEL',['NULO','BRANCO'])
            ->orderByDesc('QT_VOTOS')
            ->take(5000)
            ->get();

            $arm = $can->uniqueStrict('NM_VOTAVEL')->take($qt);
            return VotesCitiesResource2016::collection($arm);

        }else if(request()->get('ANO') == 2014 && request()->get('top_cidade') == 'cidade2014' and
        request()->get('MUNICIPIO')){
            $can = VotesCities_2014::query()
            ->whereNotIn('NM_VOTAVEL',['NULO','BRANCO'])
            ->where('NM_MUNICIPIO',request()->get('MUNICIPIO'))
            ->orderByDesc('QT_VOTOS')
            ->take(5000)
            ->get();

            $arm = $can->uniqueStrict('NM_VOTAVEL')->take($qt);
            return VotesCitiesResouce2014::collection($arm);

        }else if(request()->get('ANO') == 2014 && request()->get('top_cidade') == 'cidade2014'){
            $can = VotesCities_2014::query()
            ->whereNotIn('NM_VOTAVEL',['NULO','BRANCO'])
            ->orderByDesc('QT_VOTOS')
            ->take(5000)
            ->get();

            $arm = $can->uniqueStrict('NM_VOTAVEL')->take($qt);
            return VotesCitiesResouce2014::collection($arm);

        }else if(request()->get('ANO') == 2012 && request()->get('top_cidade') == 'cidade2012' and
        request()->get('MUNICIPIO')){
            $can = VotesCities_2012::query()
            ->whereNotIn('NM_VOTAVEL',['NULO','BRANCO'])
            ->where('NM_MUNICIPIO',request()->get('MUNICIPIO'))
            ->orderByDesc('QT_VOTOS')
            ->take(5000)
            ->get();

            $arm = $can->uniqueStrict('NM_VOTAVEL')->take($qt);
            return VotesCitiesResource2012::collection($arm);

        }else if(request()->get('ANO') == 2012 && request()->get('top_cidade') == 'cidade2012'){
            $can = VotesCities_2012::query()
            ->whereNotIn('NM_VOTAVEL',['NULO','BRANCO'])
            ->orderByDesc('QT_VOTOS')
            ->take(5000)
            ->get();

            $arm = $can->uniqueStrict('NM_VOTAVEL')->take($qt);
            return VotesCitiesResource2012::collection($arm);
        }
        else{
            return 'nothing';
        }

    }
}
